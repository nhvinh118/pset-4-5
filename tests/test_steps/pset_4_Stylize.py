from pytest_bdd import scenario, given, when, then


@scenario("stylize", "Stylize a picture")
def test_stylize_feature():
    pass

@given('I have the picture in S3')
def test_exists_picture():
    return 'picture_exists'

@given('I have fetched the picture from S3')
def test_fetched_picture():
    return 'picture_fetched'

@given('I have the model in S3')
def test_exists_model():
    return 'model_exists'

@given('I have fetched the model from S3')
def test_fetched_model():
    return 'model_fetched'

@then("I can fetch the picture from S3")
def step_impl():
    raise NotImplementedError(u'STEP: Then I can fetch the picture from S3')

@then("I can save the picture in 'data'")
def step_impl():
    raise NotImplementedError(u'STEP: Then I can save the picture in \'data\'')

@then("I can fetch the model from S3")
def step_impl():
    raise NotImplementedError(u'STEP: Then I can fetch the model from S3')

@then("I can save the model in 'data'")
def step_impl():
    raise NotImplementedError(u'STEP: Then I can save the model in \'data\'')

@then("I can stylize the picture using the model")
def step_impl():
    raise NotImplementedError(u'STEP: Then I can stylize the picture using the model')
