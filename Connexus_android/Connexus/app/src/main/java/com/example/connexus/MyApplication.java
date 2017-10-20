package com.example.connexus;

import android.app.Application;

import com.google.android.gms.auth.api.Auth;
import com.google.android.gms.auth.api.signin.GoogleSignInAccount;
import com.google.android.gms.auth.api.signin.GoogleSignInOptions;
import com.google.android.gms.common.api.GoogleApiClient;
import com.google.android.gms.common.api.Status;
import com.google.android.gms.common.api.ResultCallback;


public class MyApplication extends Application{
    private static MyApplication singleton;
    public GoogleSignInAccount mAcct;

    @Override
    public void onCreate() {
        super.onCreate();
        singleton = this;

    }

    public static synchronized MyApplication getInstance() {
        return singleton;
    }

    public void setGoogleSignInAccount(GoogleSignInAccount pGoogleApiClient) {
        this.mAcct = pGoogleApiClient;
    }

    public void resetGoogleSignInAccount() {
        this.mAcct = null;
    }

    public GoogleSignInAccount getGoogleSignInAccount() {
        if (this.mAcct != null)
            return this.mAcct;
        else
            return null;
    }

    public String test() {
        return "This is from the application";
    }
}
