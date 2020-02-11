import kivy # gotta kivy if you wanna shivvy
import re   # regular expressions for determining input
import math # for sqrt
kivy.require('1.9.1')  # necessary for _reasons_
from kivy.uix.screenmanager import Screen # the App is loaded onto the screen widget
from kivy.properties import ObjectProperty
# the ObjectProperty lets us link the CalcDisplay widget to the MainScreen in the kv file.
# it's set to None so that it just takes whatever type is assigned to it, although it could
# be specified explicity beforehand. it doesn't really matter here so I just leave it.
# there are other kinds of properties (like number, string, list, etc) that can be used
# to link values from child widgets to their parents.

from kivy.app import App # gotta app if you wanna rap
from kivy.uix.button import Button
#  Can he withstand the temptation ...to push the button that, even now, 
#  beckons him closer? Will he succumb to the maddening urge to eradicate history? 
#  At the MERE PUSH of a SINGLE BUTTON! The beeyootiful shiny button! 
#  The jolly candy-like button! Will he hold out, folks? CAN he hold out? 
from kivy.uix.textinput import TextInput 
# What's funny is that I'm not even using this for its intended purpose.

# the CalcDisplay is the disabled TextInput at the top of the calculator that shows
# the results of the calcuations. this is an old-school calculator where you can ONLY
# press the buttons, as God intended.
class CalcDisplay(TextInput):
    # here i'm precompiling all the regular expressions so I can just go ahead
    # and use them all later as I need to.
    numREComp = re.compile(r"\d")
    CEREComp  = re.compile(r"CE")
    opsREComp = re.compile(r"\÷|\×|\+|\-|\%|x\^y")
    sqrtREComp = re.compile(r"sqrt")
    decREComp = re.compile(r"\.")
    eqREComp  = re.compile(r"\=")

    # the primary buffer (the first thing you enter, before choosing an operation)
    primaryBuffer = "0"
    # the secondary buffer (the second thing you enter, after choosing an operation)
    secondaryBuffer = "0"
    # the operation of choice
    opBuffer = ""
    # whether or not an operation is in the pipe
    bufferFlag = False

    # this is the constructor that passes in all the relevant arguments
    # (through experimentation, it seems like it's necessary for linking
    # using the Properties, but i'm actually not 100% sure on that. it doesn't
    # seem to work without the initializer and the super, tho)
    def __init__(self, **kwargs):
        super(CalcDisplay, self).__init__(**kwargs)
        # set the text to the primary buffer when the widget first gets
        # set up. the buffer should always be at 0 at this point.
        self.text = self.primaryBuffer

    # when you boop a button. the event listener for this is set up in the
    # associated kv file.
    def press_button(self, buttonInput):
        # if the button pressed is a number, check if we're in the first or
        # second buffer. In either case, if we're at 0, replace the value
        # with the button's face value. If a number other than 0 is already
        # there, replace it and then start concatenating the value to the end
        # of the string.
        if(self.numREComp.match(buttonInput)):
            if(self.bufferFlag == False):
                if(self.primaryBuffer == "0"):
                    self.primaryBuffer = buttonInput
                else:
                    self.primaryBuffer += buttonInput
            else:
                if(self.secondaryBuffer == "0"):
                    self.secondaryBuffer = buttonInput
                else:
                    self.secondaryBuffer += buttonInput
        
        # this isn't implemented yet (it would add a decimal to the value)
        # luckily, that lets me demonstrate how to change a button to look
        # disabled (check the kv file; the background is different)
        if(self.decREComp.match(buttonInput)):
            pass

        # this clears all the buffers; everything starts from scratch
        if(self.CEREComp.match(buttonInput)):
            self.primaryBuffer = "0"
            self.secondaryBuffer = "0"
            self.opBuffer = ""

        # when an operation button is pressed, certain face symbols
        # can't actually be used to evaluate the result, so they get
        # switched out to the proper Python operators to be placed
        # in the operator buffer
        if(self.opsREComp.match(buttonInput)):
            if(self.bufferFlag == False):
                if(buttonInput == "÷"):
                    self.opBuffer = "/"
                elif(buttonInput == "×"):
                    self.opBuffer = "*"
                elif(buttonInput == "x^y"):
                    self.opBuffer = "**"
                else:
                    self.opBuffer= buttonInput
                self.bufferFlag = True

        # this takes the value in whichever buffer is on tap and returns its
        # square root in place. it's bugged, by the way: you can't perform the sqrt
        # operation twice in a row.
        if(self.sqrtREComp.match(buttonInput)):
            if(self.bufferFlag == False):
                self.primaryBuffer = str(math.sqrt(int(self.primaryBuffer)))
            else:
                self.secondaryBuffer = str(math.sqrt(int(self.secondaryBuffer)))

        # the equals button takes what's inside each buffer and sandwiches them
        # all together into a valid Python expression, which is then evaluated
        # and re-stringified into the output.
        if(self.eqREComp.match(buttonInput)):
            if(self.bufferFlag == True):
                fullBuffer = self.primaryBuffer + self.opBuffer + self.secondaryBuffer
                result = str(eval(fullBuffer))
                self.bufferFlag = False
                self.primaryBuffer = result
                self.secondaryBuffer = "0"
                self.opBuffer = ""
        
        # at the end of the process, update the display to reflect the primary
        # or secondary buffer
        if(self.bufferFlag == False):
            self.text = self.primaryBuffer
        else:
            self.text = self.secondaryBuffer

# defines a CalcButton. not technically necessary but useful for
# the kv file, where it's now clear where the calculator buttons are
# supposed to be
class CalcButton(Button):
    pass

# the MainScreen is a Screen widget, which is allowed to contain layout
# widgets (like BoxLayout, which is the type I'm using)
class MainScreen(Screen):
    cDisplay = ObjectProperty(None)

# this is the root of the application. the build function is apparently
# necessary and will return initialize the first screen of the application.
# the .run() method is (i think) linked to the App widget that's being passed
# in as an argument.
class KivyCalcApp(App):
    def build(self):
        ms = MainScreen()
        return ms


if __name__ == '__main__':
    KivyCalcApp().run()