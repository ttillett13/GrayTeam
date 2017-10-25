package com.example.connexus;

import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.support.annotation.NonNull;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.View;
import android.widget.AdapterView;
import android.widget.Button;
import android.widget.EditText;
import android.widget.GridView;
import android.widget.TextView;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;
import com.google.android.gms.auth.api.Auth;
import com.google.android.gms.auth.api.signin.GoogleSignInOptions;
import com.google.android.gms.common.ConnectionResult;
import com.google.android.gms.common.api.GoogleApiClient;
import com.google.android.gms.common.api.ResultCallback;
import com.google.android.gms.common.api.Status;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class ViewAllStreams extends AppCompatActivity implements
        GoogleApiClient.OnConnectionFailedListener{
    private MyApplication myApplication;
    private GoogleApiClient mGoogleApiClient;
    private Context mContext;
    private static final String TAG = MainActivity.class.getSimpleName();
    private Gson gson;
    private List<StreamPost> posts;

    private TextView title;
    private GridView imageGrid;
    private Button my_subscribed_streams;
    private Button btn_sign_out;
    private Button btn_sign_in;
    private EditText te_search_criteria;
    private Button btn_search;
    private Button btn_nearby;
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

        GsonBuilder gsonBuilder = new GsonBuilder();
        gsonBuilder.setDateFormat("yyyy-MM-dd'T'HH:mm:ss.SSSSSS");
        gson = gsonBuilder.create();

        requestQueue = Volley.newRequestQueue(this);
        fetchPosts();

    }

    /*******************************************NETWORKING CODE******************************************/
    private void fetchPosts() {
        StringRequest request = new StringRequest(Request.Method.GET, ENDPOINT, onPostsLoaded, onPostsError);
        requestQueue.add(request);
    }

    private final Response.Listener<String> onPostsLoaded = new Response.Listener<String>() {
        @Override
        public void onResponse(String response) {
            posts = Arrays.asList(gson.fromJson(response, StreamPost[].class));

            ArrayList<String> images = new ArrayList<String>();
            ArrayList<String> names = new ArrayList<String>();

            Log.i("PostActivity", posts.size() + " posts loaded.");
            for (StreamPost post : posts) {
                String fixedStr;
                fixedStr = post.url.replaceAll("127.0.0.1", "10.0.2.2");
                images.add(fixedStr);
                names.add(post.name);
            }

            for (int i = images.size(); i < 16; i++)
            {
                images.add("");
                names.add("");
            }

            String[] imageArr = new String[images.size()];
            imageArr = images.toArray(imageArr);
            String[] nameArr = new String[names.size()];
            nameArr = names.toArray(nameArr);


            GridView gridview = (GridView) findViewById(R.id.gridview);
            gridview.setAdapter(new ImageAdapter(ViewAllStreams.this, imageArr, nameArr));

            //@TIFFANY: This is where you can define an onclick for each of the images.  I have put the api call in the post.path method
           // gridview.setAdapter(new ArrayAdapter<Integer>(this,android.R.layout.simple_list_item_1, mThumbIds));
        gridview.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            public void onItemClick(AdapterView<?> parent, View v,
                                    int position, long id) {
                String name = ViewAllStreams.this.posts.get(position).name;
                /*Toast.makeText(ViewAllStreams.this, name + ": " + position,
                        Toast.LENGTH_SHORT).show(); */
                //ViewStream viewStream = new ViewStream();
                //viewStream.viewStreamPage(name);
                //viewStreamPage(name);
                Intent intent = new Intent(getApplicationContext(), ViewStream.class);
                Bundle b = new Bundle();
                b.putString("stream_name", name);
                intent.putExtras(b);
                startActivity(intent);
            }
        });

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

