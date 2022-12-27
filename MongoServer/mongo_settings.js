use admin
db.createUser(
  {
    user: "huri",
    pwd: "<Hpass>", // or cleartext password
    roles: [
      { role: "userAdminAnyDatabase", db: "admin" },
      { role: "readWriteAnyDatabase", db: "admin" }
    ]
  }
)

db.createUser(
    {
      user: "artume",
      pwd: "<Apass>", // or cleartext password
      roles: [
        { role: "readWrite", db: "toast" }
      ]
    }
)