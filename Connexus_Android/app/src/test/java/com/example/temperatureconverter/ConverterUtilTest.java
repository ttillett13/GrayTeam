package com.example.temperatureconverter;

import org.junit.Test;

import static org.junit.Assert.*;

/**
 * Created by Kapangyarihan on 10/16/17.
 */

public class ConverterUtilTest {
    @Test
    public void testConvertFahrenheitToCelsius() throws Exception {
        assertEquals("Conversion from fahrenheit to celsius failed", ConverterUtil.convertFahrenheitToCelsius(212), 100, 0.001);
    }

    @Test
    public void testConvertCelsiusToFahrenheit() throws Exception {
        assertEquals("Conversion from celsius to fahrenheit failed", ConverterUtil.convertCelsiusToFahrenheit(100), 212, 0.001);
    }
}
