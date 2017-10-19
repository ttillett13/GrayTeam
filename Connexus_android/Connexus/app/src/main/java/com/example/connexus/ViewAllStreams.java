package com.example.connexus;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.TextView;

/**
 * Created by Kapangyarihan on 10/18/17.
 */

public class ViewAllStreams extends AppCompatActivity{
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        setContentView(R.layout.view_all_streams);
//
//        // Get the Intent that started this activity and extract the string
//        Intent intent = getIntent();
//        String newString;
//        Bundle extras = intent.getExtras();
//        if(extras == null) {
//            newString= null;
//        } else {
//            newString= extras.getString("test");
//        }
//        //String message = intent.getStringExtra(MainActivity."test");
//
//        // Capture the layout's TextView and set the string as its text
//        TextView textView = (TextView) findViewById(R.id.textView);
//        textView.setText(newString);
    }

}
