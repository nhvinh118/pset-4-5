# Pset 4.5

So you are happy with your midterm test and you have finished (as usual) your problem set ("pset") weeks ahead of time. You fell in love with your achievement in the pset (and the mastery of new skills: Luigi,  Pytorch, rendering the picture of your pre-school, etc.).  You are now wondering what to do next with your free time. You are in luck!!! This pset will give you the chance to re-live all the above happy memory, while letting you indulge in your number one past time: TESTING. This exercise will give you the opportunities to refresh your knowledge of testing by focusing on Python and its test ecosystem including pytest, mock, tox and more. 

Instructor: Hoang Vinh Nguyen nguyen_h_vinh@yahoo.com>

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [Setup](#setup)
  - [Render your pset 4 repo](#render-your-pset-4-repo)
    - [Installations](#installations)
    - [AWS credentials](#aws-credentials)
  - [Styling Code](#styling-code)
    - [Fixing their work](#fixing-their-work)
  - [Pre-Trained Model & Input Content Image](#pre-trained-model--input-content-image)
  - [Limit builds on Travis](#limit-builds-on-travis)
- [Problems (45 points)](#problems-45-points)
  - [A new atomic write (10 points)](#a-new-atomic-write-10-points)
  - [External Tasks (5 points)](#external-tasks-5-points)
  - [Copying S3 files locally (15 points)](#copying-s3-files-locally-15-points)
  - [Stylizing (15 points)](#stylizing-15-points)
    - [Option A) `ExternalProgramTask`](#option-a-externalprogramtask)
    - [Option B) Direct python](#option-b-direct-python)
  - [Running it](#running-it)
  - [Your Own Image (points in quiz)](#your-own-image-points-in-quiz)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Testing in Data Sciences

## Assignment Objectives

This assignment has the following objectives:

1. Refresh for students the key concepts of testing including unit testing, integration testing and acceptance testing
2. Get the students a summary of the key concepts of testing in the specific context of Python
3. Provide the students with the opportunity to put in practice the above concepts using a selection of tools against the students own code.  

Notes:

This assignment is most effective if applied against a program that the student has successfully finished a problem set, and thus understand well the code.  In addition, in order to maximize the learning outcome of this assignment, the problem set should exhibit the following requirements:

1. The pset requires the import of the code from external libraries.  This is a good motivation for the student to quickly have a grasp of the foreign code thanks to tools like pylint or radon can help the student

2. The pset requires some data preparation before launching the application.  Alternatively (or additionally), the application can get executed with cli (command language interface).  This gives an excuse to use fixtures and mock in the testing.       

At the time of this writing, two psets come to mind: the one with luigi, pytorch and image rendering; and the coming one with Django, database, remote network.

## Problems

In the following, the assignments for the three module: unit test, integration test and acceptance test are described. For each module, the student is asked to download and get familiarized with a selective set of the tools. Information about the tools can be found in their respective home page, which is provided in the [References][References] section.

### PEP-8 and Code Analysis

Pythonistas consider as gold the style guide that Guido van Rossum, Barry Warsaw and Nick Coghlan proposed in PEP-8, one of the most famous PEPs (Python Enhancement Proposals).  Pylint is one of the linting tool that can help you determine how well your code has captured the essence of PEP-8.  Indeed, pylint is "not just a linter that annoys you!". In fact, pylint can produce a good analysis of your code, and thus helps you better prepare your unit test. A complementary tool is radon, which can generate key metrics that let you rank the complexity of your program.  This in turn helps you to risk-base your test (risk-based auditing is a term dear to regulators), while show-casing your professionalism (which does not hurt).

Task 1.1: Install **pylint** with pipenv

Task 1.2: Install **radon** with pipenv

Task 1.3: Execute pylint to get a detailed report on how compliant to PEP-8 is your code 

Task 1.4: Execute radon to obtain the key metrics of your program


### Unit Test 

You should have now a better understanding of your program.  From the analysis of the code, derive the key pointers (length, complexity, risk, etc.) from which you would want to test.  This is the ideal starting point for your unit test, which aims to cover your application at the most basic level.  Aim to cover most of the units of your code (module, class, method, function, session, etc.) and test each of them in isolation.  Note that as a developer, unit testing is squarely your responsibility.  While systematic, rigorous and thorough testing is your hallmark as an ace developer, unit testing evidences are not required from the regulatory perspectives.

Task 2.1: Install **pytest** with pipenv

Task 2.2: Install **pytest-cov** with pipenv

Task 2.3: Install **unittest.mock** with pipenv

Task 2.4: Install **tox** with pipenv

Task 2.5: With pytest, for each of the high to medium risk modules, write test cases as follows:

  1. Use assert to test key function returns in high to medium risk modules

  2. Verify key exceptions in high to medium risk modules

  3. **Fixture**:
  In this ptest context, a fixture is an environmental state or object that our test requires in order to be successful. Pytest offers a powerful decorator @pytest.fixture().  However, as discussed during Lecture, "fixtures introspect the argument name in a test function and try to find a fixture to run to inject that variable. This violates ‘explicit is better than implicit’ and makes the test cases fragile, since you can’t refactor the fixture safely".  Therefore, in order to illustrate the main merits of the concept, while not using the mechanism offered by pytest, implement the key functionalities of @pytest.fixture():  

      3.1. Separate the setup of your test from your testing by mimicking pytest's *setup_function(func)*

      3.2. Tidy up after your test has finished by mimicking pyetst's *teardown_function(func)*

      3.3. To further isolate your test, implement the above at 5 levels of scope: module, class, method, function, session 

      3.4. Use *functools.wrap()* to implement your version of @pytest.fixture(). Ensure that setup() and teardown() are respectively executed before and after the test; that the test will not start, if setup() is successful; and that teardown() is executed regardless whether the test succeeds or not.

  4. Use **coverage** to determine your coverage
    Installing pytest plugin *pytest-cov* will allow the automatic pulling of *coverage.py*, which is Python's preferred coverage method.    Extract the coverage format in HTML format to analyze your testing coverage.

Task 2.6: With **mock**, write the test cases as follows:

  1. Write a test class that mocks either of the following:

      a) the preparation of AWS CLI 

      b) the preparation of the external database

  2. [**Magic Mock**:](https://docs.python.org/3/library/unittest.mock.html#unittest.mock.MagicMock)
  *MagicMock* is a subclass of *Mock* with special support for Python's “magic methods”. In fact, *MagicMock* allows *mock* objects to replace containers or other objects and hence can support magic methods, which *should* be looked up on the class rather than the instance.
  Use *MagicMock* to test your *AtomicWrite()*:

      a) Verify that *__enter()* is correctly executed

      b) Verify that *__exit()* is correctly executed

      c) Review *moc_calls* to confirm  

Task 2.7:  With **tox**, write the test cases as follows:

  1. In *tox.ini*, ensure that your test tools of choice are properly configured (e.g., *pytest* and *pytest-cov* are used, the coverage report includes an html version, etc.)  
  
  2. Validate that your package installs correctly with different Python versions and interpreters: 2.6, 3.6 and 3.7
  
  3.  Configure *tox* to act as a front-end to a Continuous Integration server (e.g. *Jenkins* -- see below)

### Integration Test

Wikipedia defines [Integration testing](https://en.wikipedia.org/wiki/Integration_testing) as "the phase in software testing in which individual software modules are combined and tested as a group. Integration testing is conducted to evaluate the compliance of a system or component with specified functional requirements".  In the Pythonistic world, integration tends to happen frequently and often with small and incremental change.  

Martin Fowler dubbed it: 
[Continuous Integration (CI)](https://martinfowler.com/articles/continuousIntegration.html), which he defined as "a software development practice where members of a team integrate their work frequently, usually each person integrates at least daily - leading to multiple integrations per day. Each integration is verified by an automated build (including test) to detect integration errors as quickly as possible. Many teams find that this approach leads to significantly reduced integration problems and allows a team to develop cohesive software more rapidly".  CI is one of the most contentious domains from the regulatory viewpoint. Because CI is often managed and triggered by application developers, concerns are raised consequent to possible breach of segregation of duty.  To address these concerns, two key ingredients must be present: automatic testing and automated integration. This explains the role of tools such as: Buildbot, Travis CI, Jenkins CI and Docker. 

Task 3.1: Install **Buildbot** with pipenv

Task 3.2: "Install" **Travis CI**

  1. *Travis CI* is an online service. As such, there is no local software to be "installed".  However, you can install the [**Travis CI Client**](https://github.com/travis-ci/travis.rb#readme), which interfaces with both travis-ci.org and travis-ci.com.  

  2. *Configuration*: for this pset, copy your project repository in *Github* into a new *Github* repository (even though your default CI in this course is already *Travis*).

  3. *.travis.yml* is Travis-CI's configuration file.  Set your options for: notification, language, branch-specific execution steps, customized build steps (before_install, install, after_install, before_deploy, deploy, after_deploy, etc.)  

  4. **Docker** is the toolUse *Docker* in your build with *docker build* and *docker-compose*

Task 3.3: Install **Jenkins CI** with pipenv

  1. When installing *Jenkins*, add two useful plug-ins:

      a) *build-name-setter*: This plugin properly sets the display name of a build.

      b) *Test Results Analyzer*: This plugin reports the test execution results in a tabular or graphical format.

  2. Copy your project repository in *Github* into a new *Github* repository (your default CI in this course is *Travis*)

  3. Specify that a build launch is automatically triggered by a merge

  4. Build your project and analyze the build results

### Acceptance Test

In contrast to the two previous types of testing (unit test and acceptance test), acceptance test brings into the picture the most important stakeholder of your application: your clients.  Besides being the end-users of your application, they often are the one who funded your project.  In agile methodologies (extreme programming in particular), according to Wikipedia, [acceptance testing](https://en.wikipedia.org/wiki/Acceptance_testing#User_acceptance_testing) refers to "the functional testing of a user story by the software development team during the implementation phase".  In the regulatory world, the acceptance test is one of the required pieces of evidence in support of any change in the production environment.    

Task 4.1: Install **Lettuce** with pipenv

Task 4.2: Define the acceptance test in English, using the *Gherkin syntax*

Task 4.3: Define the acceptance test steps in the Python module *steps.py*

Task 4.4: Execute the acceptance test and report the results

## References

1. [Buildbot documentation](http://docs.buildbot.net/current/)
2. [Docker](https://www.docker.com/)
3. [Jenkins CI](https://jenkins.io/)
4. [Lettuce documentation](http://lettuce.it/tutorial/simple.html)
5. [unittest.mock Object Library](https://docs.python.org/3/library/unittest.mock.html)
6. [PEP-008 Style Guide for Python Code](http://legacy.python.org/dev/peps/pep-0008/)
7. [pylint homepage](https://github.com/PyCQA/pylint)
8. [pytest documentation](https://docs.pytest.org/en/latest/contents.html)
9. [Python Testing with pytest, by Brian Okken (2017)](https://www.packtpub.com/web-development/pytest-quick-start-guide)
10. [Radon documentation](https://radon.readthedocs.io/en/latest/index.html)
11. [Test-Driven Development with Python by Harry J.W. Percival (2014)](http://www.obeythetestinggoat.com/)
12. [Testing Python Unit Testing, TDD, BDD, Acceptance Testing by David Sale (2014)](https://www.wiley.com/en-us/Testing+Python%3A+Applying+Unit+Testing%2C+TDD%2C+BDD+and+Acceptance+Testing-p-9781118901229)
13. [Tox](https://tox.readthedocs.io/en/latest/index.html)
14. [Travis CI](https://docs.travis-ci.com/)
