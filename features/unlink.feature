Feature: unlink

  Scenario: unlink sub command do nothing until execute symlink
    Given there are dotfiles home directory in dotfiles
    And dotfiles home directory contains no files
    And home directory contains some files
    When we run dotfav unlink
    Then home directory does not changed
