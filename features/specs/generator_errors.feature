Feature: GeneratorErrors
  As a user
  I want to be able to reliably use the generator and see errors when bad values are entered
  In order to easily populates my assessments without crashs

  Scenario: Trying to create a problem with wrong parameters
    Given I am logged with a fresh class, created a test and accessed question generator
    # Incorrect number of decimals
    Then I chose "-10" decimals
    When I click on the create button
    Then I see an error panel
    # Negative Number of questions required
    Then I chose "2" decimals
    Then I chose to generate "-10" questions
    When I click on the create button
    Then I see an error panel
    # Volume Errors
    Then I chose to generate "5" questions
    Then I select the volume problem generator
    Then I select the object cylinder
    When I click on the create button
    Then I see an error panel
    Then I chose to generate "10" questions
    Then I enter "60" as lower range and "2" as upper range
    When I click on the create button
    Then I see an error panel
    Then I chose to generate "10" questions
    Then I enter "1" as lower range and "1" as upper range
    When I click on the create button
    Then I see an error panel
    Then I chose to generate "10" questions
    Then I enter "0" as lower range and "60" as upper range
    When I click on the create button
    Then I see an error panel
    # Arithmetics
    Then I select the arithmetic problem generator
    When I click on the create button
    Then I see an error panel
    Then I chose to generate "10" questions
    Then I enter "9999" as lower range and "-1" as upper range
    When I click on the create button
    Then I see an error panel
    Then I chose to generate "10" questions
    Then I enter "0" as lower range and "1" as upper range
    When I click on the create button
    Then I see an error panel
    # Statistics
    Then I select the statistic problem generator
    When I click on the create button
    Then I see an error panel
    Then I chose to generate "10" questions
    Then I enter "50" elements asked
    Then I enter "99999" as lower range and "-1" as upper range
    When I click on the create button
    Then I see an error panel
    Then I chose to generate "10" questions
    Then I enter "0" as lower range and "0" as upper range
    When I click on the create button
    Then I see an error panel
    Then I chose to generate "10" questions
    Then I enter "1" elements asked
    Then I enter "0" as lower range and "60" as upper range
    When I click on the create button
    Then I see an error panel
    # Pythagoras Errors
    Then I select the pythagoras problem generator
    When I click on the create button
    Then I see an error panel
    Then I chose to generate "10" questions
    Then I enter "99999" as lower range and "-1" as upper range
    When I click on the create button
    Then I see an error panel
    Then I chose to generate "10" questions
    Then I enter "0" as lower range and "0" as upper range
    When I click on the create button
    Then I see an error panel
    Then I chose to generate "10" questions
    Then I enter "-3" as lower range and "60" as upper range
    When I click on the create button
    Then I see an error panel
    # Area errors
    Then I select the area problem generator
    Then I chose to generate "10" questions
    Then I select the object rhombus
    Then I see an error panel
    Then I enter "99999" as lower range and "-1" as upper range
    When I click on the create button
    Then I see an error panel
    Then I chose to generate "10" questions
    Then I enter "0" as lower range and "0" as upper range
    When I click on the create button
    Then I see an error panel
    Then I chose to generate "10" questions
    Then I enter "-3" as lower range and "60" as upper range
    When I click on the create button
    Then I see an error panel
    # Perimeter errors
    Then I select the perimeter problem generator
    Then I chose to generate "10" questions
    Then I select the object rhombus
    Then I see an error panel
    Then I enter "99999" as lower range and "-1" as upper range
    When I click on the create button
    Then I see an error panel
    Then I chose to generate "10" questions
    Then I enter "0" as lower range and "0" as upper range
    When I click on the create button
    Then I see an error panel
    Then I chose to generate "10" questions
    Then I enter "-3" as lower range and "60" as upper range
    When I click on the create button
    Then I see an error panel