Feature: Login
  As a user
  I want to be able to login into the site
  In order to use its functionality

  Scenario: Login as a professor

    Given I am an existing non logged professor
    Given I am on the login page
    Then I enter my username
    When I submit my username
    Then I am on the password page
    Then I enter my password
    When I submit my password
    Then I am redirected to the professor home page

  Scenario: Login with wrong password
    Given I am an existing non logged professor
    Given I am on the login page
    Then I enter my username
    When I submit my username
    Then I am on the password page
    Then I enter an invalid password
    When I submit my password
    Then I am redirected to the login fail page

  Scenario: Login with wrong username
    Given I am an existing non logged professor
    Given I am on the login page
    Then I enter an invalid username
    When I submit my username
    Then I am redirected to the login fail page