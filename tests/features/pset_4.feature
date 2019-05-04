# Created by hoang at 5/4/19
Feature: Stylize
  As a graphic designer,
    I want to stylize a given picture,
    So I can embellish this picture,
    Using the graphic pattern from a model that my client has chosen.

  Scenario: Picture fetching
    Given I have the picture in S3
      And I have provided AWS_ACCESS_KEY
      And I have provide AWS_SECRET_KEY
      Then I can fetch the picture from S3

  Scenario: Picture saving
    Given I have fetched the picture from S3
      And I have created the local folder 'data'
      Then I can save the picture in 'data'

  Scenario: Model fetching
    Given I have the model in S3
      And I have provided AWS_ACCESS_KEY
      And I have provide AWS_SECRET_KEY
      Then I can fetch the model from S3

  Scenario: Model saving
    Given I have fetched the model from S3
      And I have created the local folder 'data'
      Then I can save the model in 'data'

  Scenario: Picture stylizing
    Given I have saved the picture in 'data'
      And I have saved the model in 'data'
      Then I can stylize the picture using the model
