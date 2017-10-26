package com.example.connexus.activities;


import android.Manifest;
import android.content.Context;
import android.content.pm.PackageManager;
import android.location.Location;
import android.os.Bundle;
import android.support.annotation.NonNull;
import android.support.v4.app.ActivityCompat;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.GridView;
import android.widget.Toast;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;
import com.example.connexus.ImageAdapter;
import com.example.connexus.MainActivity;
import com.example.connexus.R;
import com.example.connexus.beans.NearbyModel;
import com.example.connexus.beans.SearchStreamModel;
import com.google.android.gms.common.ConnectionResult;
import com.google.android.gms.common.api.GoogleApiClient;
import com.google.android.gms.location.LocationServices;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Calendar;
import java.util.List;

public class NearbyStreams extends AppCompatActivity implements GoogleApiClient.ConnectionCallbacks, GoogleApiClient.OnConnectionFailedListener, ActivityCompat.OnRequestPermissionsResultCallback {
    private Context mContext;
    private static final String TAG = MainActivity.class.getSimpleName();
    private Gson gson;
    private List<NearbyModel> posts;


    private GridView gv_allStreams;
    private Button btn_More, btn_MoreResult;
    private static final String ENDPOINT = "http://10.0.2.2:8080/ViewAllStream/api";


    private RequestQueue requestQueue;
    private String CurEndpoint;

    GoogleApiClient mGoogleApiClient;
    private Location mLastLocation;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.near_by_streams);

        gv_allStreams = (GridView) findViewById(R.id.gv_allStreams);
        btn_More = (Button) findViewById(R.id.btn_More);
        btn_MoreResult = (Button) findViewById(R.id.btn_MoreResult);

        btn_MoreResult.setVisibility(View.GONE);

        GsonBuilder gsonBuilder = new GsonBuilder();
        gsonBuilder.setDateFormat("yyyy-MM-dd'T'HH:mm:ss.SSSSSS");
        gson = gsonBuilder.create();

        requestQueue = Volley.newRequestQueue(this);
//           fetchPosts();

        initLocation();

        btn_More.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                posts=null;
                //fillData();
                processGridData();
            }
        });
    }


    private void initLocation() {
        mGoogleApiClient = new GoogleApiClient.Builder(this)
                .addConnectionCallbacks(this)
                .addOnConnectionFailedListener(this)
                .addApi(LocationServices.API).build();
        mGoogleApiClient.connect();
    }


    @Override
    public void onConnectionFailed(ConnectionResult result) {
        Log.i(TAG, "Connection failed: ConnectionResult.getErrorCode() = " + result.getErrorCode());
    }

    @Override
    public void onConnected(Bundle arg0) {
        processCurrentLocation();
    }

    @Override
    public void onConnectionSuspended(int arg0) {
        mGoogleApiClient.connect();
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        processCurrentLocation();
    }

    private void processCurrentLocation(){
        if (ActivityCompat.checkSelfPermission(this, Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED && ActivityCompat.checkSelfPermission(this, Manifest.permission.ACCESS_COARSE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
            ActivityCompat.requestPermissions(this, new String[]{Manifest.permission.ACCESS_FINE_LOCATION},111);
            return;
        }
        mLastLocation = LocationServices.FusedLocationApi.getLastLocation(mGoogleApiClient);
        if (mLastLocation != null) {
            Toast.makeText(this, mLastLocation.getLatitude() + " : "+mLastLocation.getLongitude(), Toast.LENGTH_LONG).show();

        }
        CurEndpoint = ENDPOINT + "?longitude=" +mLastLocation.getLongitude() +";latitude=" + mLastLocation.getLatitude();
        processGridData();
    }

    @Override
    protected void onPause() {
        super.onPause();
        mGoogleApiClient.disconnect();
    }

    @Override
    protected void onResume() {
        super.onResume();
        mGoogleApiClient.connect();
    }

    /*******************************************NETWORKING CODE******************************************/
    private void fetchPosts() {
        StringRequest request = new StringRequest(Request.Method.GET, CurEndpoint, onPostsLoaded, onPostsError);
        requestQueue.add(request);
    }

    private final Response.Listener<String> onPostsLoaded = new Response.Listener<String>() {
        @Override
        public void onResponse(String response) {
            posts = Arrays.asList(gson.fromJson(response, NearbyModel[].class));
            processGridData();
        }
    };

    private final Response.ErrorListener onPostsError = new Response.ErrorListener() {
        @Override
        public void onErrorResponse(VolleyError error) {
            Log.e("PostActivity", error.toString());
        }
    };

    private NearbyModel getDummyData(int rndNo){
        NearbyModel ssm = new NearbyModel();
        ssm.datetime = Calendar.getInstance().getTime();
        ssm.name = "Name - "+rndNo;
        ssm.path = "/ViewSingleStream?stream_name=Nature Stream";
        ssm.url =  "http://127.0.0.1:8080/_ah/img/encoded_gs_file:c3RhZ2luZy52aWJyYW50LW1pbmQtMTc3NjIzLmFwcHNwb3QuY29tL1BpY3R1cmVzL0tvYWxhLmpwZw==";
        ssm.distance = (rndNo*2)+"";
        return ssm;
    }
    private void processGridData(){

        if(posts==null){
            posts = new ArrayList<>();
            for(int i=0;i<10;i++){
                posts.add(getDummyData(i));
            }
        }
        ArrayList<String> images = new ArrayList<String>();
        ArrayList<String> names = new ArrayList<String>();

        Log.i("PostActivity", posts.size() + " posts loaded.");
        for (NearbyModel post : posts) {
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


        gv_allStreams.setAdapter(new ImageAdapter(NearbyStreams.this, imageArr, nameArr));
    }
}

