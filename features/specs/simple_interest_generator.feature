Feature: SimpleInterestGenerator
  As a user
  I want to be able to automatically creates simple interest questions
  In order to easily populates my assessments

  Scenario: Successfully creating an simple interest problem with time in month and monthly rate
    Given I am logged with a fresh class, created a test and accessed question generator
    Then I select the simple interest problem generator
    Then I set the time placed to "month"
    Then I set the type of rate to "month"
    When I click on the create button
    Then I see a list of generated problems
    Then I choose a generated problem
    Then I click on going back to the test

  Scenario: Successfully creating an simple interest problem with time in year and annual rate
    Given I am logged with a fresh class, created a test and accessed question generator
    Then I select the simple interest problem generator
    Then I set the time placed to "year"
    Then I set the type of rate to "year"
    When I click on the create button
    Then I see a list of generated problems
    Then I choose a generated problem
    Then I click on going back to the test

  Scenario: Successfully creating an simple interest problem with time in year and monthly rate
    Given I am logged with a fresh class, created a test and accessed question generator
    Then I select the simple interest problem generator
    Then I set the time placed to "year"
    Then I set the type of rate to "month"
    When I click on the create button
    Then I see a list of generated problems
    Then I choose a generated problem
    Then I click on going back to the test

  Scenario: Successfully creating an simple interest problem with time in month and annual rate
    Given I am logged with a fresh class, created a test and accessed question generator
    Then I select the simple interest problem generator
    Then I set the time placed to "month"
    Then I set the type of rate to "year"
    When I click on the create button
    Then I see a list of generated problems
    Then I choose a generated problem
    Then I click on going back to the test