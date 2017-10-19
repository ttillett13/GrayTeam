package com.example.connexus;

import android.app.Application;

import com.google.android.gms.auth.api.Auth;
import com.google.android.gms.auth.api.signin.GoogleSignInOptions;
import com.google.android.gms.common.api.GoogleApiClient;


public class MyApplication extends Application{
    private static MyApplication singleton;
    public GoogleApiHelper googleApiHelper;
    public GoogleApiClient mGoogleApiClient;

    @Override
    public void onCreate() {
        super.onCreate();
        singleton = this;

        googleApiHelper = new GoogleApiHelper(singleton);

    }

    public static synchronized MyApplication getInstance() {
        return singleton;
    }

    public GoogleApiHelper getGoogleApiHelperInstance() {
        return this.googleApiHelper;
    }

    public static GoogleApiHelper getGoogleApiHelper() {
        return getInstance().getGoogleApiHelperInstance();
    }

    public void setGoogleApiClient(GoogleApiClient pGoogleApiClient) {
        this.mGoogleApiClient = pGoogleApiClient;
    }

    public GoogleApiClient getGoogleApiClient() {

        return this.mGoogleApiClient;
    }

    public String test() {
        return "This is from the application";
    }
}
