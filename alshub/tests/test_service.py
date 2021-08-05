from alshub.service import alshub_roles_to_beamline_groups


def test_get_beamline_roles():
    roles_response = {
                    "FirstName": "Zaphod",
                    "LastName": "Beabelbrox",
                    "ORCID": "0000-0002-1817-0042X",
                    "Beamline Roles": [
                        {
                            "beamline1": [
                                "Scientist",
                                "Beamline Usage",
                                "Satisfaction Survey",
                                "Scheduler",
                                "Beamline Staff",
                                "Experiment Authorization",
                                "RAC Beamline Admin"
                            ]
                        },
                        {
                            "beamline2": [
                                "Beamline Staff"
                            ]
                        }
                    ]
                }
    beamlines = alshub_roles_to_beamline_groups(roles_response["Beamline Roles"])
    assert len(beamlines) == 1
    assert beamlines[0] == "beamline1"

    beamlines = alshub_roles_to_beamline_groups([])
    assert len(beamlines) == 0
