DELETE FROM bandplannerapi_setlistsong WHERE id > 9

DROP TABLE bandplannerapi_banduser

DELETE FROM auth_user WHERE id > 1

DELETE FROM bandplannerapi_banduser WHERE id > 1

DELETE FROM authtoken_token WHERE user_id > 1