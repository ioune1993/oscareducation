Feature: AreaGenerator
  As a user
  I want to be able to automatically creates area questions
  In order to easily populates my assessments

  Scenario: Successfully creating an area rhombus problem
    Given I am logged with a fresh class, created a test and accessed question generator
    Then I select the area problem generator
    Then I chose to generate "10" questions
    Then I select the object rhombus
    Then I enter "1" as lower range and "60" as upper range
    When I click on the create button
    Then I see a list of generated problems
    Then I choose a generated problem
    Then I click on going back to the test

  Scenario: Successfully creating an area rectangle problem
    Given I am logged with a fresh class, created a test and accessed question generator
    Then I select the area problem generator
    Then I chose to generate "10" questions
    Then I select the object rectangle
    Then I enter "1" as lower range and "60" as upper range
    When I click on the create button
    Then I see a list of generated problems
    Then I choose a generated problem
    Then I click on going back to the test

  Scenario: Successfully creating an area square problem
    Given I am logged with a fresh class, created a test and accessed question generator
    Then I select the area problem generator
    Then I chose to generate "10" questions
    Then I select the object square
    Then I enter "1" as lower range and "60" as upper range
    When I click on the create button
    Then I see a list of generated problems
    Then I choose a generated problem
    Then I click on going back to the test

  Scenario: Successfully creating an area triangle problem
    Given I am logged with a fresh class, created a test and accessed question generator
    Then I select the area problem generator
    Then I chose to generate "10" questions
    Then I select the object triangle
    Then I enter "1" as lower range and "60" as upper range
    When I click on the create button
    Then I see a list of generated problems
    Then I choose a generated problem
    Then I click on going back to the test

  Scenario: Successfully creating an area trapezium problem
    Given I am logged with a fresh class, created a test and accessed question generator
    Then I select the area problem generator
    Then I chose to generate "10" questions
    Then I select the object trapezium
    Then I enter "1" as lower range and "60" as upper range
    When I click on the create button
    Then I see a list of generated problems
    Then I choose a generated problem
    Then I click on going back to the test

  Scenario: Successfully creating an area quadrilateral problem
    Given I am logged with a fresh class, created a test and accessed question generator
    Then I select the area problem generator
    Then I chose to generate "10" questions
    Then I select the object quadrilateral
    Then I enter "1" as lower range and "60" as upper range
    When I click on the create button
    Then I see a list of generated problems
    Then I choose a generated problem
    Then I click on going back to the test

  Scenario: Successfully creating an area circle problem
    Given I am logged with a fresh class, created a test and accessed question generator
    Then I select the area problem generator
    Then I chose to generate "10" questions
    Then I select the object circle
    Then I enter "1" as lower range and "60" as upper range
    When I click on the create button
    Then I see a list of generated problems
    Then I choose a generated problem
    Then I click on going back to the test

  Scenario: Successfully creating an area parallelogram problem
    Given I am logged with a fresh class, created a test and accessed question generator
    Then I select the area problem generator
    Then I chose to generate "10" questions
    Then I select the object parallelogram
    Then I enter "1" as lower range and "60" as upper range
    When I click on the create button
    Then I see a list of generated problems
    Then I choose a generated problem
    Then I click on going back to the test

  Scenario: Successfully creating an area regular polygon problem
    Given I am logged with a fresh class, created a test and accessed question generator
    Then I select the area problem generator
    Then I chose to generate "10" questions
    Then I select the object regular polygon
    Then I enter "1" as lower range and "60" as upper range
    When I click on the create button
    Then I see a list of generated problems
    Then I choose a generated problem
    Then I click on going back to the test