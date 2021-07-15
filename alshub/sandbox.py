from splash_userservice.models import (
    User
)

users = []
users.append(User(**{
    "uid": "42",
    "given_name": "ford",
    "family_name": "prefect",
    "groups": ["beetlguice", "earth"],
    "orcid": "0000-0002-3580-328X"
}))
