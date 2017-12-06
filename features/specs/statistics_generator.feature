Feature: StatisticsGenerator
  As a user
  I want to be able to automatically creates statistic questions
  In order to easily populates my assessments

  Scenario: Successfully creating an statistic problem
    Given I am logged with a fresh class, created a test and accessed question generator
    Then I select the statistic problem generator
    Then I enter "50" elements asked
    Then I enter "0" as lower range and "60" as upper range
    When I click on the create button
    Then I see a list of generated problems
    Then I choose a generated problem
    Then I click on going back to the test