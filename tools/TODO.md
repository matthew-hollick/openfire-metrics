# TODO


## All tools where appropriate

New CLI options:
  - servicename as a filter for which chatrooms to consider. default should be empty as this appears to include chatrooms from all services

url cli option:
  - should be split into: 
    - "openfire_api" which should look like: "https://chat.gbr.uk:9091" and by default is "http://localhost:9090"
    - "openfire_path" which by default is "/plugins/restapi/v1"

General:
  - Tools should not re-implement functions already defined under openfire_api
  - All tools should process cli options using click. the options should be consistent across tools. the help should be consistent across tools.

---

## chatrooms_tool.py

Existing fields:
  - "creationDate" should be a nice iso timestamp
  - "modificationDate" should be a nice iso timestamp

New fields:
  - "message_count" as returned by a count of http://localhost:9090/plugins/restapi/v1/chatrooms/[CHAT_ROOM]/chathistory?servicename=conference this has the potential to get large.
  - "occupants_count" as a count of occupants
  - "members_count" as a count of members

---

## users_tool.py

option to filter on field "email" not null

New fields:
  - "statistics.total.count" the count of users
  - "statistics.total.logged_on" the count of users where field "logged_on" is true
  - "statistics.local.count" the count of users where field "local_user" is true
  - "statistics.local.logged_on" the count of users where field "local_user" is true and field "logged_on" is true
  - "statistics.remote.count" the count of users where field "local_user" is false
  - "statistics.remote.logged_on" the count of users where field "local_user" is false and field "logged_on" is true


