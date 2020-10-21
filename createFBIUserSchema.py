import csv
import sys
import configparser
import requests
import warnings
warnings.filterwarnings("ignore")


# Read the config file to retrieve url and token
config = configparser.ConfigParser()
config.read('okta-config.txt')
URL = config.get('General', 'url')
token = config.get('General', 'token')


# function to create FBI Member UserType in Okta
def createFBIUserType ():

    # preparing the Create User JSON BODY

    jsonTosend = {
        "description": "FBI Member specific profile",
        "displayName": "FBI Member",
        "name": "fbi_user"
    }

    # Call the create user type API
    res = requests.post(URL + '/api/v1/meta/types/user',
                        headers={'Accept': 'application/json', 'Content-Type': 'application/json',
                                 'Authorization': 'SSWS ' + token}, json=jsonTosend,verify=False)

    # Retrieving the user Type ID to be passed to the addCustomAttributesforFBIUser function
    dictFromServer = res.json()
    url=(dictFromServer['_links']['schema']['href'])
    id = url.split('/')[-1]

    # Calling the function for adding custom attributes to the FBI Member UserType
    addCustomAttributesforFBIUser(id)

# function to create custom attributes for the FBI Member UserType
def addCustomAttributesforFBIUser (id):
    jsonTosend = {
    "definitions": {
        "custom": {
            "id": "#custom",
            "type": "object",
            "properties": {
                "divisions": {
                    "title": "Division",
                    "type": "array",
                    "required": True,
                    "mutability": "READ_WRITE",
                    "scope": "NONE",
                    "items": {
                        "type": "string",
                        "enum": [
                            "D1",
                            "D2",
                            "D3",
                            "D4",
                            "D5"
                        ],
                        "oneOf": [
                            {
                                "const": "D1",
                                "title": "Masonry"
                            },
                            {
                                "const": "D2",
                                "title": "GC"
                            },
                            {
                                "const": "D3",
                                "title": "HVY Civil"
                            },
                            {
                                "const": "D4",
                                "title": "Electrical"
                            },
                            {
                                "const": "D5",
                                "title": "Mechanical"
                            }
                        ]
                    },
                    "union": "DISABLE",
                    "permissions": [
                        {
                            "principal": "SELF",
                            "action": "READ_WRITE"
                        }
                    ],
                    "master": {
                        "type": "PROFILE_MASTER"
                    }
                },
                "company": {
                    "title": "Company",
                    "type": "array",
                    "required": True,
                    "mutability": "READ_WRITE",
                    "scope": "NONE",
                    "items": {
                        "type": "string",
                        "enum": [
                            "C1",
                            "C2",
                            "C3",
                            "C4",
                            "C5",
                            "C6"
                        ],
                        "oneOf": [
                            {
                                "const": "C1",
                                "title": "Buckeye Construction and Restoration"
                            },
                            {
                                "const": "C2",
                                "title": "Market & Johnson"
                            },
                            {
                                "const": "C3",
                                "title": "Lang Masonry"
                            },
                            {
                                "const": "C4",
                                "title": "Wolf Creek Contracting"
                            },
                            {
                                "const": "C5",
                                "title": "KBS Constructors"
                            },
                            {
                                "const": "C6",
                                "title": "Q & D Construction"
                            }
                        ]
                    },
                    "union": "DISABLE",
                    "permissions": [
                        {
                            "principal": "SELF",
                            "action": "READ_WRITE"
                        }
                    ],
                    "master": {
                        "type": "PROFILE_MASTER"
                    }
                },
                "roundtable_group": {
                    "title": "Roundtable",
                    "type": "array",
                    "required": True,
                    "mutability": "READ_WRITE",
                    "scope": "NONE",
                    "items": {
                        "type": "string",
                        "enum": [
                            "RT1",
                            "RT2",
                            "RT3",
                            "RT4",
                            "RT5",
                            "RT6",
                            "RT7",
                            "RT8",
                            "RT9",
                            "RT10"
                        ],
                        "oneOf": [
                            {
                                "const": "RT1",
                                "title": "Nashville Group"
                            },
                            {
                                "const": "RT2",
                                "title": "Columbus Group"
                            },
                            {
                                "const": "RT3",
                                "title": "Tacoma Group"
                            },
                            {
                                "const": "RT4",
                                "title": "Lake Charles Group"
                            },
                            {
                                "const": "RT5",
                                "title": "Goldsboro Group"
                            },
                            {
                                "const": "RT6",
                                "title": "SBG Group"
                            },
                            {
                                "const": "RT7",
                                "title": "Charlotte Group"
                            },
                            {
                                "const": "RT8",
                                "title": "Oregon Trail Group"
                            },
                            {
                                "const": "RT9",
                                "title": "Kansas City Group"
                            },
                            {
                                "const": "RT10",
                                "title": "Newport News Group"
                            }
                        ]
                    },
                    "union": "DISABLE",
                    "permissions": [
                        {
                            "principal": "SELF",
                            "action": "READ_WRITE"
                        }
                    ],
                    "master": {
                        "type": "PROFILE_MASTER"
                    }
                },
                "role_code": {
                    "title": "Role",
                    "type": "string",
                    "required": True,
                    "mutability": "READ_WRITE",
                    "scope": "NONE",
                    "enum": [
                        "EXT1"
                    ],
                    "oneOf": [
                        {
                            "const": "EXT1",
                            "title": "FBI Member"
                        }
                    ],
                    "permissions": [
                        {
                            "principal": "SELF",
                            "action": "READ_WRITE"
                        }
                    ],
                    "master": {
                        "type": "PROFILE_MASTER"
                    }
                }
            }
}
    }
}

    # Call the add custom attribute API
    res = requests.post(URL + '/api/v1/meta/schemas/user/'+id,headers={'Accept': 'application/json', 'Content-Type': 'application/json','Authorization': 'SSWS ' + token}, json=jsonTosend,verify=False)


# function to create FBI Member Admin UserType
def createFBIMemberAdminUserType ():

    # preparing the Create User Type JSON body

    jsonTosend = {
        "description": "schema for FBI Member Admin",
        "displayName": "FBI Member Admin",
        "name": "fbi_member_admin"
    }

    # Call the create user type API
    res = requests.post(URL + '/api/v1/meta/types/user',
                        headers={'Accept': 'application/json', 'Content-Type': 'application/json',
                                 'Authorization': 'SSWS ' + token}, json=jsonTosend,verify=False)

    # Retrieving the user Type ID to be passed to the addCustomAttributesforFBIMemberAdmin function
    dictFromServer = res.json()
    url=(dictFromServer['_links']['schema']['href'])
    id = url.split('/')[-1]
    addCustomAttributesforFBIMemberAdmin(id)

# function to add custom attributes for the FBI Member Admin UserType
def addCustomAttributesforFBIMemberAdmin (id):
    jsonTosend = {
    "definitions": {
        "custom": {
            "id": "#custom",
            "type": "object",
            "properties": {
                "divisions": {
                    "title": "Division Administrator",
                    "type": "array",
                    "required": True,
                    "mutability": "READ_WRITE",
                    "scope": "NONE",
                    "items": {
                        "type": "string",
                        "enum": [
                            "D1",
                            "D2",
                            "D3",
                            "D4",
                            "D5"
                        ],
                        "oneOf": [
                            {
                                "const": "D1",
                                "title": "Masonry"
                            },
                            {
                                "const": "D2",
                                "title": "GC"
                            },
                            {
                                "const": "D3",
                                "title": "HVY Civil"
                            },
                            {
                                "const": "D4",
                                "title": "Electrical"
                            },
                            {
                                "const": "D5",
                                "title": "Mechanical"
                            }
                        ]
                    },
                    "union": "DISABLE",
                    "permissions": [
                        {
                            "principal": "SELF",
                            "action": "READ_WRITE"
                        }
                    ],
                    "master": {
                        "type": "PROFILE_MASTER"
                    }
                },
                "company": {
                    "title": "Company",
                    "type": "array",
                    "required": True,
                    "mutability": "READ_WRITE",
                    "scope": "NONE",
                    "items": {
                        "type": "string",
                        "enum": [
                            "C1",
                            "C2",
                            "C3",
                            "C4",
                            "C5",
                            "C6"
                        ],
                        "oneOf": [
                            {
                                "const": "C1",
                                "title": "Buckeye Construction and Restoration"
                            },
                            {
                                "const": "C2",
                                "title": "Market & Johnson"
                            },
                            {
                                "const": "C3",
                                "title": "Lang Masonry"
                            },
                            {
                                "const": "C4",
                                "title": "Wolf Creek Contracting"
                            },
                            {
                                "const": "C5",
                                "title": "KBS Constructors"
                            },
                            {
                                "const": "C6",
                                "title": "Q & D Construction"
                            }
                        ]
                    },
                    "union": "DISABLE",
                    "permissions": [
                        {
                            "principal": "SELF",
                            "action": "READ_WRITE"
                        }
                    ],
                    "master": {
                        "type": "PROFILE_MASTER"
                    }
                },
                "roundtable_group": {
                    "title": "Roundtable",
                    "type": "array",
                    "required": True,
                    "mutability": "READ_WRITE",
                    "scope": "NONE",
                    "items": {
                        "type": "string",
                        "enum": [
                            "RT1",
                            "RT2",
                            "RT3",
                            "RT4",
                            "RT5",
                            "RT6",
                            "RT7",
                            "RT8",
                            "RT9",
                            "RT10"
                        ],
                        "oneOf": [
                            {
                                "const": "RT1",
                                "title": "Nashville Group"
                            },
                            {
                                "const": "RT2",
                                "title": "Columbus Group"
                            },
                            {
                                "const": "RT3",
                                "title": "Tacoma Group"
                            },
                            {
                                "const": "RT4",
                                "title": "Lake Charles Group"
                            },
                            {
                                "const": "RT5",
                                "title": "Goldsboro Group"
                            },
                            {
                                "const": "RT6",
                                "title": "SBG Group"
                            },
                            {
                                "const": "RT7",
                                "title": "Charlotte Group"
                            },
                            {
                                "const": "RT8",
                                "title": "Oregon Trail Group"
                            },
                            {
                                "const": "RT9",
                                "title": "Kansas City Group"
                            },
                            {
                                "const": "RT10",
                                "title": "Newport News Group"
                            }
                        ]
                    },
                    "union": "DISABLE",
                    "permissions": [
                        {
                            "principal": "SELF",
                            "action": "READ_WRITE"
                        }
                    ],
                    "master": {
                        "type": "PROFILE_MASTER"
                    }
                },
                "role_code": {
                    "title": "Role",
                    "type": "string",
                    "required": True,
                    "mutability": "READ_WRITE",
                    "scope": "NONE",
                    "enum": [
                        "EXT2"
                    ],
                    "oneOf": [
                        {
                            "const": "EXT2",
                            "title": "FBI Member Admin"
                        }
                    ],
                    "permissions": [
                        {
                            "principal": "SELF",
                            "action": "READ_WRITE"
                        }
                    ],
                    "master": {
                        "type": "PROFILE_MASTER"
                    }
                }
            }
}
    }
}

    # Call the add custom attribute API
    res = requests.post(URL + '/api/v1/meta/schemas/user/'+id,headers={'Accept': 'application/json', 'Content-Type': 'application/json','Authorization': 'SSWS ' + token}, json=jsonTosend,verify=False)


createFBIUserType()
createFBIMemberAdminUserType()