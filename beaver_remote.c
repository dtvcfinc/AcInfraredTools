#include <stdio.h>
#include "irslinger.h"

int main(int argc, char *argv[])
{
	uint32_t outPin = 3;            // The Broadcom pin number the signal will be sent on
	int frequency = 38000;           // The frequency of the IR signal in Hz
	double dutyCycle = 0.5;          // The duty cycle of the IR signal. 0.5 means for every cycle,
	                                 // the LED will turn on for half the cycle time, and off the other half
	int leadingPulseDuration = 3000; // The duration of the beginning pulse in microseconds
	int leadingGapDuration = 1500;   // The duration of the gap in microseconds after the leading pulse
	int onePulse = 350;              // The duration of a pulse in microseconds when sending a logical 1
	int zeroPulse = 350;             // The duration of a pulse in microseconds when sending a logical 0
	int oneGap = 1150;               // The duration of the gap in microseconds when sending a logical 1
	int zeroGap = 350;               // The duration of the gap in microseconds when sending a logical 0
	int sendTrailingPulse = 1; 


	int result = irSling(
		outPin,
		frequency,
		dutyCycle,
		leadingPulseDuration,
		leadingGapDuration,
		onePulse,
		zeroPulse,
		oneGap,
		zeroGap,
		sendTrailingPulse,
		argv[1]);	
	return result;
}
