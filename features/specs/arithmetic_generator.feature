Feature: ArithmeticGenerator
  As a user
  I want to be able to automatically creates arithmetical polynomial questions
  In order to easily populates my assessments

  Scenario: Successfully creating an arithmetic problem
    Given I am logged with a fresh class, created a test and accessed question generator
    Then I select the arithmetic problem generator
    Then I enter "0" as lower range and "60" as upper range
    When I click on the create button
    Then I see a list of generated problems
    Then I choose a generated problem
    Then I click on going back to the test

  Scenario: Successfully creating an arithmetic problem with rational domain
    Given I am logged with a fresh class, created a test and accessed question generator
    Then I select the arithmetic problem generator
    Then I enter "0" as lower range and "60" as upper range
    Then I select the rational domain
    When I click on the create button
    Then I see a list of generated problems
    Then I choose a generated problem
    Then I click on going back to the test