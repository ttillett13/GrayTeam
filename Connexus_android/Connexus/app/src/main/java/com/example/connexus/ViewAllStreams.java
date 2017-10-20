package com.example.connexus;


import android.support.annotation.NonNull;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.GridLayout;
import android.widget.Space;
import android.widget.TextView;

import com.google.android.gms.auth.api.Auth;
import com.google.android.gms.auth.api.signin.GoogleSignInOptions;
import com.google.android.gms.common.ConnectionResult;
import com.google.android.gms.common.SignInButton;
import com.google.android.gms.common.api.GoogleApiClient;
import com.google.android.gms.common.api.ResultCallback;
import com.google.android.gms.common.api.Status;

/**
 * Created by Kapangyarihan on 10/18/17.
 */

public class ViewAllStreams extends AppCompatActivity implements
        GoogleApiClient.OnConnectionFailedListener{
    private MyApplication myApplication;
    private GoogleApiClient mGoogleApiClient;
    private static final String TAG = MainActivity.class.getSimpleName();

    private TextView title;
    private GridLayout grid_layout;
    private Button my_subscribed_streams;
    private Button btn_sign_out;
    private Button btn_sign_in;
    private EditText te_search_criteria;
    private Button btn_search;
    private Button btn_nearby;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.view_all_streams);

        myApplication = (MyApplication)getApplicationContext();
        title = (TextView) findViewById(R.id.title);
        grid_layout = (GridLayout) findViewById(R.id.grid_layout);
        my_subscribed_streams = (Button) findViewById(R.id.my_subscribed_streams);
        btn_sign_out = (Button) findViewById(R.id.btn_sign_out);
        btn_sign_in = (Button) findViewById(R.id.btn_sign_in);
        te_search_criteria = (EditText) findViewById(R.id.te_search_criteria);
        btn_search = (Button) findViewById(R.id.btn_search);
        btn_nearby = (Button) findViewById(R.id.btn_nearby);


        GoogleSignInOptions gso = new GoogleSignInOptions.Builder(GoogleSignInOptions.DEFAULT_SIGN_IN)
                .requestEmail()
                .build();

        mGoogleApiClient = new GoogleApiClient.Builder(this)
                .enableAutoManage(this, this)
                .addApi(Auth.GOOGLE_SIGN_IN_API, gso)
                .build();

        if (myApplication.getGoogleSignInAccount() != null)
            updateUI(true);
        else
            updateUI(false);
    }

    public void signIn(View view) {
        finish();
    }

    public void signOut(View view) {
        myApplication.resetGoogleSignInAccount();
        Auth.GoogleSignInApi.signOut(mGoogleApiClient).setResultCallback(
                new ResultCallback<Status>() {
                    @Override
                    public void onResult(Status status) {
                        finish();
                    }
                });
    }

    @Override
    public void onConnectionFailed(@NonNull ConnectionResult connectionResult) {
        // An unresolvable error has occurred and Google APIs (including Sign-In) will not
        // be available.
        Log.d(TAG, "onConnectionFailed:" + connectionResult);
    }

    private void updateUI(boolean isSignedIn) {
        getSupportActionBar().setDisplayHomeAsUpEnabled(false);
        getSupportActionBar().setHomeButtonEnabled(false);
        if (isSignedIn) {
            title.setVisibility(View.VISIBLE);
            grid_layout.setVisibility(View.VISIBLE);
            my_subscribed_streams.setVisibility(View.VISIBLE);
            btn_sign_out.setVisibility(View.VISIBLE);
            btn_sign_in.setVisibility(View.GONE);
            te_search_criteria.setVisibility(View.VISIBLE);
            btn_search.setVisibility(View.VISIBLE);
            btn_nearby.setVisibility(View.VISIBLE);
        } else {
            title.setVisibility(View.VISIBLE);
            grid_layout.setVisibility(View.VISIBLE);
            my_subscribed_streams.setVisibility(View.GONE);
            btn_sign_out.setVisibility(View.GONE);
            btn_sign_in.setVisibility(View.VISIBLE);
            te_search_criteria.setVisibility(View.VISIBLE);
            btn_search.setVisibility(View.VISIBLE);
            btn_nearby.setVisibility(View.VISIBLE);
        }
    }
}
