package com.example.connexus;


import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.drawable.Drawable;
import android.support.annotation.NonNull;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.GridLayout;
import android.widget.GridView;
import android.widget.ImageView;
import android.widget.Space;
import android.widget.TextView;
import android.widget.Toast;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;
import com.bumptech.glide.Glide;
import com.google.android.gms.auth.api.Auth;
import com.google.android.gms.auth.api.signin.GoogleSignInOptions;
import com.google.android.gms.common.ConnectionResult;
import com.google.android.gms.common.SignInButton;
import com.google.android.gms.common.api.GoogleApiClient;
import com.google.android.gms.common.api.ResultCallback;
import com.google.android.gms.common.api.Status;
import com.google.gson.annotations.SerializedName;

import org.json.JSONObject;

import java.net.URL;
import java.util.ArrayList;
import java.util.Date;

/**
 * Created by Kapangyarihan on 10/18/17.
 */

public class ViewAllStreams extends AppCompatActivity implements
        GoogleApiClient.OnConnectionFailedListener{
    private MyApplication myApplication;
    private GoogleApiClient mGoogleApiClient;
    private Context mContext;
    private static final String TAG = MainActivity.class.getSimpleName();
    private ArrayList<Bitmap> bitmapList;

    private TextView title;
    private GridView imageGrid;
    private Button my_subscribed_streams;
    private Button btn_sign_out;
    private Button btn_sign_in;
    private EditText te_search_criteria;
    private Button btn_search;
    private Button btn_nearby;
    //private static final String ENDPOINT = "https://kylewbanks.com/rest/posts.json";
    private static final String ENDPOINT = "http://10.0.2.2:8080/ViewAllStream/api";


    private RequestQueue requestQueue;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.view_all_streams);

        myApplication = (MyApplication)getApplicationContext();
        title = (TextView) findViewById(R.id.title);
        imageGrid = (GridView) findViewById(R.id.gridview);
        my_subscribed_streams = (Button) findViewById(R.id.my_subscribed_streams);
        btn_sign_out = (Button) findViewById(R.id.btn_sign_out);
        btn_sign_in = (Button) findViewById(R.id.btn_sign_in);
        te_search_criteria = (EditText) findViewById(R.id.te_search_criteria);
        btn_search = (Button) findViewById(R.id.btn_search);
        btn_nearby = (Button) findViewById(R.id.btn_nearby);
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




//
//        this.imageGrid.setAdapter(new ImageAdapter(this, this.bitmapList));
//
//
//
//
//
//
//        requestQueue = Volley.newRequestQueue(this);
//        fetchPosts();

        // references to our images


        GridView gridview = (GridView) findViewById(R.id.gridview);
        gridview.setAdapter(new ImageAdapter(ViewAllStreams.this, images));
        //gridview.setAdapter(new ArrayAdapter<Integer>(this,android.R.layout.simple_list_item_1, mThumbIds));

//        gridview.setOnItemClickListener(new AdapterView.OnItemClickListener() {
//            public void onItemClick(AdapterView<?> parent, View v,
//                                    int position, long id) {
//                Toast.makeText(ViewAllStreams.this, "" + position,
//                        Toast.LENGTH_SHORT).show();
//            }
//        });















    }

    private Bitmap urlImageToBitmap(String imageUrl) throws Exception {
        Bitmap result = null;
        URL url = new URL(imageUrl);
        if(url != null) {
            result = BitmapFactory.decodeStream(url.openConnection().getInputStream());
        }
        return result;
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
    public void goBackToLogin(View view) {
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
        Log.d(TAG, "onConnectionFailed:" + connectionResult);
    }

    private void updateUI(boolean isSignedIn) {
        getSupportActionBar().setDisplayHomeAsUpEnabled(false);
        getSupportActionBar().setHomeButtonEnabled(false);
        if (isSignedIn) {
            title.setVisibility(View.VISIBLE);
            imageGrid.setVisibility(View.VISIBLE);
            my_subscribed_streams.setVisibility(View.VISIBLE);
            btn_sign_out.setVisibility(View.VISIBLE);
            btn_sign_in.setVisibility(View.GONE);
            te_search_criteria.setVisibility(View.VISIBLE);
            btn_search.setVisibility(View.VISIBLE);
            btn_nearby.setVisibility(View.VISIBLE);
        } else {
            title.setVisibility(View.VISIBLE);
            imageGrid.setVisibility(View.VISIBLE);
            my_subscribed_streams.setVisibility(View.GONE);
            btn_sign_out.setVisibility(View.GONE);
            btn_sign_in.setVisibility(View.VISIBLE);
            te_search_criteria.setVisibility(View.VISIBLE);
            btn_search.setVisibility(View.VISIBLE);
            btn_nearby.setVisibility(View.VISIBLE);
        }
    }
    /*******************************************END LOGIN CODE********************************************/
}


//
//class Post {
//
//    @SerializedName("id")
//    long ID;
//
//    @SerializedName("date")
//    Date lastUpdate;
//
//    String name;
//    String imagePath;
//    String url;
//}

