from py42 import sdk
from py42.constants import WatchlistType
from py42.exceptions import Py42WatchlistNotFound, Py42NotFoundError

instance = "https://console.us.code42.com"
username = "phantomlab@splunk.com"
password = "PHcode052942;!;22"
sdk = sdk.from_local_account(
    instance, username, password
)
# 1116310945009257293, 1069773342011620484
watchlist_id_example = "c66b842d-566e-4b7f-8af2-4cb5f7154821"
user_id_example = "1116311141487233869"
username_example= "abc123@gmail.com"




# get watchlist member
response = sdk.watchlists.get_watchlist_member(watchlist_id_example, user_id_example)
print(response.data)

# # get user profile
# response = sdk.users.get_by_username(username_example)
# print(response)



# print("_____________________________________________________________________")

# # get user profile using user id
# response = sdk.users.get_by_uid(user_id_example)
# print(response)

# response = sdk.userriskprofile.get_by_id(user_id_example)
# print(response)


# list all the users in watchlist
# response = sdk.watchlists.get_all_included_users(watchlist_id_example)
# # print(response)
# for data in response:
#     print(data.status_code)


# add user to watchlists
# try:
#     response = sdk.watchlists.add_included_users_by_watchlist_type(["1116310945009257293"], "DEPARTING_EMPLOYEE")
#     print(response.data)
#     print(response.status_code)
# except Py42NotFoundError as e:
#     print(e)

# try:
#     response = sdk.watchlists.delete("82bb5b31-4cea-49fc-ae8f-25cca1caa2d1123123123")
#     print(response.data)
#     print(response.status_code)
# except Exception as e:
#     print(e)

# try:
#     watchlist = sdk.watchlists.create(
#         # WatchlistType.CUSTOM
#         title="testHardik123123!@#$%^&***FXGCHVBNM.,';LJKHJGHCGJKLIJHKGJHVBJL,M MM,N,KNLKHSDFKNGLKSDNFLHSNDFVSLKNDFVLKKSXCLV AKSVCLKNFKLJQJKSDFKKJJKBK",
#         description="description123@#$%^&*()" 
#     )
# except Py42Error as e:
#     print(e)
# print(watchlist.data)



# get specific watclists
# try:
#     response = sdk.watchlists.get(watchlist_id_example)
#     print(response.data)
# except Py42WatchlistNotFound as err:
#     print(err.response.status_code)



# # list all the watchlists
# watchlists_response = sdk.watchlists.get_all()
# for page in watchlists_response:
#     final_response = page.data
#     print(final_response)
#     print("////__________________________________________________////")

# total_count =  page.data.get("totalCount")
# print(total_count)


# CODE42V2_WATCHLIST_TYPE_LIST = {
#     "contractor" : "CONTRACT_EMPLOYEE",
#     "departing" : "DEPARTING_EMPLOYEE",
#     "elevated_access" : "ELEVATED_ACCESS_PRIVILEGES",
#     "flight_risk" : "FLIGHT_RISK",
#     "high_impact" : "HIGH_IMPACT_EMPLOYEE",
#     "new_hire" : "NEW_EMPLOYEE",
#     "performance_concerns" : "PERFORMANCE_CONCERNS",
#     "poor_security_practices" : "POOR_SECURITY_PRACTICES",
#     "suspicious_system_activity" : "SUSPICIOUS_SYSTEM_ACTIVITY",
#     "custom" : "CUSTOM",
# }



# code42_list_data = [
#     "contractor",
#     "departing",
#     "elevated_access",
#     "flight_risk",
#     "high_impact",
#     "new_hire",
#     "performance_concerns",
#     "poor_security_practices",
#     "suspicious_system_activity",
#     "custom"
# ]



# print(CODE42V2_WATCHLIST_TYPE_LIST.get("custom", None))


#{'listType': 'CONTRACT_EMPLOYEE', 'watchlistId': '8a48c93c-95f3-40aa-9c8d-4a409a45351c', 'tenantId': '1b9ade82-6f5d-4f19-a2e8-c47c18ed9021', 'stats': {}}


#{'listType': 'CUSTOM', 'watchlistId': 'eba75f8b-6295-46ba-8a67-b5a341e1f6e5', 'tenantId': '1b9ade82-6f5d-4f19-a2e8-c47c18ed9021', 'title': 'testHardik123123!@#$%^&***', 'description': 'description123@#$%^&*()', 'stats': {}}