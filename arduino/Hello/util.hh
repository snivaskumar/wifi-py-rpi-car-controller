/* Copyright 2017 Francis James Franklin
 * 
 * Open Source under the MIT License - see LICENSE in the project's root folder
 */

#ifndef ArduinoHello_util_hh
#define ArduinoHello_util_hh

#include <Arduino.h>

/* Specifically for printing a string stored in program memory (using PROGMEM),
 * with the option of a trailing newline.
 * 
 * Suppress printing if echo is off.
 */
extern void print_pgm (const char * str_pgm); // adds a newline automatically at the end

/* Suppress printing if echo is off.
 */
extern void print_str (const char * str);
extern void print_char (char c);

/* Turn echo on/off
 */
extern void echo (bool bOn);

/* Input parsing
 */
extern void input_check (); // check for input, and handle as necessary
extern void input_reset (); // reset the input buffer

enum CommandStatus {
  cs_Okay = 0,
  cs_UnknownCommand,
  cs_IncorrectUsage,
  cs_InvalidPin
};

/* Set callback functions for user command & interrupt
 */
extern void set_user_interrupt (void (*user_interrupt) ());
extern void set_user_command (CommandStatus (*user_command) (int argc, char ** argv));

#endif /* !ArduinoHello_util_hh */