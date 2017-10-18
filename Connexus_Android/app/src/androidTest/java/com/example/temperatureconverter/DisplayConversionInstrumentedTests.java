package com.example.temperatureconverter;

//import com.example.contextmock.util;
import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;

import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;

import static junit.framework.Assert.assertEquals;
import static junit.framework.Assert.assertNotNull;
import static org.mockito.Mockito.mock;

import com.example.temperatureconverter.MainActivity.*;

/**
 * Created by Kapangyarihan on 10/16/17.
 */
@RunWith(MockitoJUnitRunner.class)
public class DisplayConversionInstrumentedTests {
    @Test
    public void constructDisplayIntentCtoF() throws Exception {
        Context context = mock(Context.class);
        Intent intent = MainActivity.buildIntent(context, String.valueOf(ConverterUtil.convertCelsiusToFahrenheit(100.0f)));
        assertNotNull(intent);
        Bundle extras = intent.getExtras();
        assertNotNull(extras);
        assertEquals("212.0", extras.getString("message"));
    }

    @Test
    public void constructDisplayIntentFtoC() throws Exception {
        Context context = mock(Context.class);
        Intent intent = MainActivity.buildIntent(context, String.valueOf(ConverterUtil.convertFahrenheitToCelsius(212.0f)));
        assertNotNull(intent);
        Bundle extras = intent.getExtras();
        assertNotNull(extras);
        assertEquals("100.0", extras.getString("message"));
    }

}
