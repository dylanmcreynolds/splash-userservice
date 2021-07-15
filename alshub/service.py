import asyncio
import logging
import ssl
from typing import List
from pprint import pprint

from httpx import AsyncClient, codes

from splash_userservice.models import User, AccessGroup
from splash_userservice.service import IDType, UserService, UserNotFound
from .sandbox import users

ALSHUB_BASE = "https://alsusweb.lbl.gov:1024"
ALSHUB_PERSON = "ALSGetPerson"
ALSHUB_PROPOSAL = "ALSUserProposals"
ALSHUB_PROPOSALBY = "ALSGetProposalsBy"

logger = logging.getLogger("users.alshub")

context = ssl.create_default_context()
context.load_verify_locations(cafile="./incommonrsaca.pem")


staff = {
    "dyparkinson@lbl.gov": ["bl832"],
    "dmcreynolds@lbl.gov": ["bl832"],
    "ahexemer@lbl.gov": ["bl832"],
    "hkrishnan@lbl.gov": ["bl832"],
}


class ALSHubService(UserService):
    """Implementation of splash_userservice backed by http calls to ALSHub

    Parameters
    ----------
    splash_userservice : [type]
        [description]
    """
    is_orcid_sandbox = False

    def __init__(self, is_orcid_sandbox=False) -> None:
        self.is_orcid_sandbox = is_orcid_sandbox
        super().__init__()

    async def get_user(self, id: str, id_type: IDType) -> User:
        """Return a user object from ALSHub. Makes several calls to ALSHub to assemble user info
        and proposal info, which is used to populate group names.

        Parameters
        ----------
        orcid : str
            User's orcid

        Returns
        -------
        User
            User instance populate with info from ALSHub requests
        """

        if self.is_orcid_sandbox:
            for user in users:
                if id_type == IDType.orcid and user.orcid == id:
                    return user

        async with AsyncClient(base_url=ALSHUB_BASE, verify=context, timeout=10.0) as ac:
            # query for user information
            if id_type == IDType.email:
                q_param = "em"
            else:
                q_param = "or"
            response = await ac.get(f"{ALSHUB_PERSON}/?{q_param}={id}")

            if response.status_code == 404:
                raise UserNotFound(f'user {id} not found in ALSHub')
            if response.status_code != codes.OK:
                info('error getting user: %s status code: %s message: %s',
                     id,
                     response.status_code, response.json())
                return None

            user_response_obj = response.json()
            user_lb_id = user_response_obj.get('LBNLID')
            if not user_lb_id:
                raise UserNotFound(f'user {id} not found in ALSHub or could not communicate')
            info('get_user userinfo for orcid: %s  lbid: %s',
                 id,
                 user_lb_id)

            # query for proposals by lblid, which will become groups
            groups = []
            response = await ac.get(f"{ALSHUB_PROPOSALBY}/?lb={user_lb_id}")
            if response.status_code != codes.OK:
                info('error getting user proposals: %s status code: %s message: %s', 
                     user_lb_id,
                     response.status_code,
                     response.json())
            else:
                proposal_response_obj = response.json()
                proposals = proposal_response_obj.get('Proposals')
                if not proposals:
                    info('no proposals for lbnlid: %s', user_response_obj.get('LBNLID'))
                else: 
                    info('get_user userinfo for orcid: %s proposals: %s', 
                         id, 
                         str(proposals)) 
                
                    groups = [proposal_id for proposal_id in proposals]
            
            # add staff beamlines to groups list
            if id_type == IDType.email:
                beamlines = await self.get_staff_beamlines(id)
                groups = groups + beamlines
            return User(**{
                "uid": user_response_obj.get('LBNLID'),
                "given_name": user_response_obj.get('FirstName'),
                "family_name": user_response_obj.get('LastName'),
                "current_institution": user_response_obj.get('Institution'),
                "current_email": user_response_obj.get('OrgEmail'),
                "orcid": user_response_obj.get('orcid'),
                "groups": groups
            })

    async def get_staff_beamlines(self, email: str) -> List[str]:
        beamlines = staff.get(email)
        if beamlines:
            info(f"Adding beamlines {beamlines} for user {email}")
            return beamlines
        return []

    async def get_user_proposals(self, orcid: str) -> List[AccessGroup]:
        # query by orcid just to get lbl id
        user = await self.get_user(orcid)
        info('get_user_accessgroups userinfo for orcid %s', orcid)
        async with AsyncClient(base_url=ALSHUB_BASE, verify=context, timeout=10.0) as ac:
            response = await ac.get(f"{ALSHUB_PROPOSAL}/?em={user.current_email}")
            response_obj = response.json()
            groups = []
            for proposal in response_obj.get('Proposals'):
                groups.append(AccessGroup(**{
                    "uid": proposal.get('ExpID'),
                    "name": proposal.get('ExpID')           
                }))
            return groups


def info(log, *args):
    if logger.isEnabledFor(logging.INFO):
        logger.info(log, *args)


async def main():
    logger.setLevel(logging.DEBUG)
    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)
    service = ALSHubService()

    user = await service.get_user("0000-0002-3979-8844")
    access_groups = await service.get_user_proposals("0000-0002-3979-8844")
    
    pprint(user)

    print("============")
    pprint(access_groups)

if __name__ == "__main__":
    asyncio.run(main())
