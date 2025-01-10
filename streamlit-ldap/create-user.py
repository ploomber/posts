from ldap3 import Server, Connection, MODIFY_REPLACE, SUBTREE, ALL_ATTRIBUTES

# Connect to the LDAP server
server = Server("ldap://localhost:389")
conn = Connection(server, "cn=admin,dc=example,dc=com", "admin", auto_bind=True)

# Create new user
user_dn = "cn=Test User,dc=example,dc=com"
object_class = ["top", "person", "organizationalPerson", "inetOrgPerson"]

attributes = {
    "cn": "Test User",
    "sn": "User",
    "uid": "testuser",
    "userPassword": "password123",
    "displayName": "Test User",
    "title": "Developer",
}

# Add the new user
conn.add(user_dn, object_class, attributes)

print(f"User creation {'successful' if conn.result['result'] == 0 else 'failed'}")
conn.unbind()
