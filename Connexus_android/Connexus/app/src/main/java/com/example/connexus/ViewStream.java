package com.example.connexus;

import android.content.Context;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.os.Bundle;
import android.support.annotation.NonNull;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.GridView;
import android.widget.TextView;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.google.android.gms.auth.api.Auth;
import com.google.android.gms.auth.api.signin.GoogleSignInOptions;
import com.google.android.gms.common.ConnectionResult;
import com.google.android.gms.common.api.GoogleApiClient;

import java.net.URL;
import java.util.ArrayList;

public class ViewStream extends AppCompatActivity implements
        GoogleApiClient.OnConnectionFailedListener{

    private MyApplication myApplication;
    private GoogleApiClient mGoogleApiClient;
    private Context mContext;
    private static final String TAG = MainActivity.class.getSimpleName();
    private ArrayList<Bitmap> bitmapList;

    private TextView title;
    private GridView imageGrid;
    private Button btn_view_streams;
    private Button btn_upload;
    private Button my_subscribed_streams;
    private Button btn_sign_out;
    private Button btn_sign_in;
    private EditText te_search_criteria;
    private Button btn_search;
    private Button btn_nearby;
    //private static final String ENDPOINT = "https://kylewbanks.com/rest/posts.json";
    private static final String ENDPOINT = "http://10.0.2.2:8080/ViewStream/api";


    private RequestQueue requestQueue;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.view_stream);

        myApplication = (MyApplication)getApplicationContext();
        title = (TextView) findViewById(R.id.title);
        imageGrid = (GridView) findViewById(R.id.gridview2);
        btn_view_streams = (Button) findViewById(R.id.btn_view_streams);
        btn_upload = (Button) findViewById(R.id.btn_upload);
        this.bitmapList = new ArrayList<Bitmap>();


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



        String[] images = {
                "http://i.imgur.com/rFLNqWI.jpg",
                "http://i.imgur.com/C9pBVt7.jpg",
                "http://i.imgur.com/rT5vXE1.jpg",
                "http://i.imgur.com/aIy5R2k.jpg",
                "http://i.imgur.com/MoJs9pT.jpg",
                "http://i.imgur.com/S963yEM.jpg",
                "http://i.imgur.com/rLR2cyc.jpg",

        };


        GridView gridview = (GridView) findViewById(R.id.gridview);
        gridview.setAdapter(new ImageAdapter(ViewStream.this, images));

    }

    private Bitmap urlImageToBitmap(String imageUrl) throws Exception {
        Bitmap result = null;
        URL url = new URL(imageUrl);
        if(url != null) {
            result = BitmapFactory.decodeStream(url.openConnection().getInputStream());
        }
        return result;
    }


    public void uploadImage(View view) {
        Intent intent = new Intent(this, ViewStream.class);
        startActivity(intent);
    }

    public void uploadImage() {
        Intent intent = new Intent(this, ViewStream.class);
        startActivity(intent);
    }

    /*******************************************NETWORKING CODE******************************************/
    private void fetchPosts() {
        StringRequest request = new StringRequest(Request.Method.GET, ENDPOINT, onPostsLoaded, onPostsError);
        requestQueue.add(request);
    }

    private final Response.Listener<String> onPostsLoaded = new Response.Listener<String>() {
        @Override
        public void onResponse(String response) {
            Log.i("PostActivity", response);
        }
    };

    private final Response.ErrorListener onPostsError = new Response.ErrorListener() {
        @Override
        public void onErrorResponse(VolleyError error) {
            Log.e("PostActivity", error.toString());
        }
    };
    /****************************************END OF NETWORKING CODE**************************************/

    /*********************************************LOGIN CODE*********************************************/

    @Override
    public void onConnectionFailed(@NonNull ConnectionResult connectionResult) {
        Log.d(TAG, "onConnectionFailed:" + connectionResult);
    }

    private void updateUI(boolean isSignedIn) {
        getSupportActionBar().setDisplayHomeAsUpEnabled(false);
        getSupportActionBar().setHomeButtonEnabled(false);
        if (isSignedIn) {
            title.setVisibility(View.VISIBLE);
            imageGrid.setVisibility(View.VISIBLE);
            btn_sign_out.setVisibility(View.VISIBLE);
            btn_sign_in.setVisibility(View.GONE);
            btn_upload.setVisibility(View.VISIBLE);
            btn_view_streams.setVisibility(View.VISIBLE);
        } else {
            title.setVisibility(View.VISIBLE);
            imageGrid.setVisibility(View.VISIBLE);
            my_subscribed_streams.setVisibility(View.GONE);
            btn_sign_out.setVisibility(View.GONE);
            btn_sign_in.setVisibility(View.VISIBLE);
            btn_upload.setVisibility(View.VISIBLE);
            btn_view_streams.setVisibility(View.VISIBLE);
        }
    }
    /*******************************************END LOGIN CODE********************************************/
}


