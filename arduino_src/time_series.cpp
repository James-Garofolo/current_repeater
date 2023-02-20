#include <Arduino.h>

const int verbose = 0; // 0 = just levels, 1 = just process, 2 = process and action

const int sample = 2, sample_not = 3, drain = 4, latch = 5, level = 6; // digital pins

const int sampling = 13, latching = 12, draining = 11, sending = 10, leveling = 9; // feedback digital pins

const int sampled = 0, latched = 1, current = 2, level_feedback = 3, in_current = 4; // analog pins

int received_v, a = 0, count, last_count = 0, last_v = 0, level_v = 0; // internal variables

int sample_current(int verbose);
void latch_v(int verbose);
void drain_cap(int verbose);
int sample_and_send(int which);
void balance_output(int count, int last_count);


void setup() {
    pinMode(sample, OUTPUT);
    pinMode(sample_not, OUTPUT);
    pinMode(drain, OUTPUT);
    pinMode(latch, OUTPUT);
    pinMode(level, OUTPUT);
    Serial.begin(115200);
    //pinMode(sampling, OUTPUT);
    //pinMode(latching, OUTPUT);
    //pinMode(draining, OUTPUT);
    //pinMode(sending, OUTPUT);
    //pinMode(leveling, OUTPUT);

    /**/

    digitalWrite(sample_not, HIGH);
    digitalWrite(sample, LOW);
    digitalWrite(drain, LOW);
    digitalWrite(latch, LOW);

    while (1) {//for(a = 0; a<15; a++){
        a++;
        Serial.println(a);
        if (verbose > 0) {
            Serial.println("lvl");
        }

        while (abs(count - last_count) < 20) {
            count = rand() % 200;
        }

        balance_output(count, last_count);
        //Serial.println(count);
        last_count = count;
        //sample_and_send(in_current);

        if (verbose > 0) {
            Serial.println("smp");
        }
        //sample_and_send(in_current);
        sample_current(verbose);
        latch_v(verbose);
        //sample_and_send(in_current);
    }

    Serial.println("end");
}

void loop() {}



int sample_and_send(int which) {
    int sample;

    switch (which) {
    case sampled:
        Serial.print("s,");
        break;
    case latched:
        Serial.print("l,");
        break;
    case current:
        Serial.print("o,");
        break;
    case in_current:
        Serial.print("c,");
        break;
    }

    Serial.print(micros());
    Serial.print(",");
    sample = analogRead(which);
    Serial.println(sample);
    return sample;
}


void drain_cap(int verbose) {
    int sample_v;
    if (verbose == 2) {
        Serial.println("draining");
    }

    digitalWrite(sample, LOW);
    sample_v = analogRead(sampled);//sample_and_send(sampled);
    digitalWrite(drain, HIGH);
    while (sample_v > 0) {
        sample_v = analogRead(sampled);//sample_and_send(sampled);
    }
    digitalWrite(drain, LOW);

}

void latch_v(int verbose) {
    int latched_val, sample_val;
    if (verbose == 2) {
        Serial.println("latching");
    }

    digitalWrite(latch, HIGH);
    do {
        sample_val = analogRead(sampled);//sample_and_send(sampled);
        latched_val = analogRead(latched);//sample_and_send(latched);
        //sample_and_send(current);
        //sample_and_send(in_current);
    } while (latched_val != sample_val);
    digitalWrite(latch, LOW);

}

int sample_current(int verbose) {
    if (verbose == 2) {
        Serial.println("sampling");
    }
    //sample_and_send(in_current);
    //sample_and_send(sampled);
    //Serial.print("s,");
    //t = micros();

    digitalWrite(sample_not, LOW);
    digitalWrite(sample, HIGH);
    delayMicroseconds(4000);
    //lvl = analogRead(sampled);
    //for(i=0; i<3; i++){
    //    sample_and_send(sampled);
    //}
    digitalWrite(sample, LOW);
    digitalWrite(sample_not, HIGH);

    //Serial.print(t);
    //Serial.print(",");
    //Serial.println(lvl);
    //sample_and_send(in_current);

    return analogRead(sampled);//sample_and_send(sampled);
}

void balance_output(int count, int last_count) {
    int fbk, i_in, match_cnt = 0;
    analogWrite(level, count); // set the level of the input laser
    drain_cap(verbose); // drain the sample cap

    if (verbose > 1) {
        Serial.print(count);
        Serial.print(",");
        Serial.println(last_count);
    }

    if (count > last_count) {
        do { // wait until the voltage is at a steady state
            last_v = level_v;
            delay(2);
            level_v = analogRead(level_feedback);
            if ((level_v < last_v) || (level_v == 0)) {
                match_cnt++;
            }
        } while (match_cnt < 3);
    }
    else {
        do { // wait until the voltage is at a steady state
            last_v = level_v;
            delay(2);
            level_v = analogRead(level_feedback);
            if ((level_v > last_v) || (level_v == 0)) {
                match_cnt++;
            }
        } while (match_cnt < 3);
    }

    if (verbose > 1) {
        Serial.println("matching");
    }

    match_cnt = 0;
    do {
        fbk = analogRead(level_feedback);
        i_in = analogRead(in_current);//sample_and_send(in_current);
        if (fbk == i_in) {
            match_cnt++;
        }
        //delayMicroseconds(100);
        //sample_and_send(latched);
        //sample_and_send(current);
        //sample_and_send(sampled);
    } while (match_cnt < 3);
    /*
    if (count > last_count){
        do{ // wait until the voltage is at a steady state
            last_v = level_v;
            delay(2);
            //level_v = analogRead(level_feedback);
            level_v = sample_and_send(in_current);
            sample_and_send(latched);
            sample_and_send(current);
        } while (level_v >= last_v);
    } else{
        do{ // wait until the voltage is at a steady state
            last_v = level_v;
            delay(2);
            //level_v = analogRead(level_feedback);
            level_v = sample_and_send(in_current);
            sample_and_send(latched);
            sample_and_send(current);
        } while (level_v <= last_v);
    }
    */
}