package com.example.temperatureconverter;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.EditText;
import android.widget.RadioButton;
import android.widget.TextView;
import android.widget.Toast;

public class MainActivity extends Activity {
    private EditText text;
    public static final String EXTRA_MESSAGE = "com.example.temperatureconverter.MESSAGE";
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        text = (EditText) findViewById(R.id.inputValue);

    }

    // this method is called at button click because we assigned the name to the
    // "OnClick" property of the button
    public void onClick(View view) {
        String message = "ERROR";
        switch (view.getId()) {
            case R.id.button1:
                RadioButton celsiusButton = (RadioButton) findViewById(R.id.radio0);
                RadioButton fahrenheitButton = (RadioButton) findViewById(R.id.radio1);

                float inputValue = Float.parseFloat(text.getText().toString());
                if (celsiusButton.isChecked()) {
                    celsiusButton.setChecked(false);
                    fahrenheitButton.setChecked(true);
                    message = text.getText() + "C is " + ConverterUtil.convertCelsiusToFahrenheit(inputValue) + "F";


                } else {
                    fahrenheitButton.setChecked(false);
                    celsiusButton.setChecked(true);
                    message = text.getText() + "F is " + ConverterUtil.convertFahrenheitToCelsius(inputValue) + "C";

                }
                break;
        }

            Intent intent = buildIntent(this, message);
            startActivity(intent);
        }

    public static Intent buildIntent(Context activity, String message)
    {
        Intent intent = new Intent(activity, DisplayConversion.class);
        //TextView textView = (TextView) findViewById(R.id.TemperatureString);
        intent.putExtra("message", message);
        return intent;
    }
    }