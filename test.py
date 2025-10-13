from fastapi_testrunner import TestFastAPIRoutes

test = TestFastAPIRoutes()
test.start_test()




#api key , client secret, configuration [otp,google],redirect url "http://api.senseai.com/redirect" =>given by DeB-Auth

#post /auth json={'apikey':'yourapikey'} => http://auth.debuggers.com/auth/login/1234-5678-9876

#opening the returned link into browser

# aftere login it will redirect with code http://senseai/redirect?code=123456

#post /authenticated-user json={'code':123456,client_secret:'yourclientsecret'}

#jwt token => email,name,profile_pic

