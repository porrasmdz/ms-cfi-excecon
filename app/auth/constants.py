#Could go from database
RESOURCES_FOR_ROLES = {
    "admin": {
        "resource1": ['read', 'write', 'delete'],
        "resource2": ["read", "write"],
    },
    "user": {
        "resource1": ["read"],
        "resource2": ["read", "write"],
    }
}
# Optionally, define paths to be excluded from checking for permissions
EXCLUDED_PATHS = ["docs", "auth" ,"openapi.json"]
