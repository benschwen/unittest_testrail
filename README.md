# unittest_testrail
A nice and easy integration between python unittest and test rail - using decorators for test attributes, base_test module, and global configuration for the means of integrating test runs into test rail.  The goal of this was to make it as easy as possible to estabilish how your test methods integrate into test runs in testrail.  Another goal was to make our test classes very pretty and easy to read while still having full test rail support.  I think you'll find this project does that quite well.  

## USAGE
you'll want to start by looking at **test_controller.py** and **framework/base_test.py** to get examples of how this is used.
you'll find many examples of how this can be applied to a selenium framework, or any other popular automation methods.

see test_modules/../..py **for usage of attributes on test methods**

-- this was originally written for integration with selenium and saucelabs 
 - you will find some commented out code for saucelabs, including support for logging videos
 - you will find some basic selenium framework support including screenshots and logging them



##### USE AS YOUR TEST FRAMEWORK STARTING POINT, OR COPY WHAT YOU LIKE AND DITCH THE REST
makes no difference to me.  just leave your feedback on the github page!  thanks!


### if you'd like to add things to this and push into my repo, go for it!!!  
