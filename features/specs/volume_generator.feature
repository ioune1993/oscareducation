Feature: VolumeGenerator
  As a user
  I want to be able to automatically creates volume questions
  In order to easily populates my assessments

  Scenario: Successfully creating an volume problem for a cone
    Given I am logged with a fresh class, created a test and accessed question generator
    Then I select the volume problem generator
    Then I select the object cone
    Then I enter "1" as lower range and "60" as upper range
    When I click on the create button
    Then I see a list of generated problems
    Then I choose a generated problem
    Then I click on going back to the test

  Scenario: Successfully creating an volume problem for a prism
    Given I am logged with a fresh class, created a test and accessed question generator
    Then I select the volume problem generator
    Then I select the object prism
    Then I enter "1" as lower range and "60" as upper range
    When I click on the create button
    Then I see a list of generated problems
    Then I choose a generated problem
    Then I click on going back to the test

  Scenario: Successfully creating an volume problem for a cube
    Given I am logged with a fresh class, created a test and accessed question generator
    Then I select the volume problem generator
    Then I select the object cube
    Then I enter "1" as lower range and "60" as upper range
    When I click on the create button
    Then I see a list of generated problems
    Then I choose a generated problem
    Then I click on going back to the test

  Scenario: Successfully creating an volume problem for a pyramid
    Given I am logged with a fresh class, created a test and accessed question generator
    Then I select the volume problem generator
    Then I select the object pyramid
    Then I enter "1" as lower range and "60" as upper range
    When I click on the create button
    Then I see a list of generated problems
    Then I choose a generated problem
    Then I click on going back to the test

  Scenario: Successfully creating an volume problem for a cylinder
    Given I am logged with a fresh class, created a test and accessed question generator
    Then I select the volume problem generator
    Then I select the object cylinder
    Then I enter "1" as lower range and "60" as upper range
    When I click on the create button
    Then I see a list of generated problems
    Then I choose a generated problem
    Then I click on going back to the test