package com.example.connexus;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.ImageView;

import com.squareup.picasso.Picasso;


public class ViewImageAdapter extends BaseAdapter {
    private Context mContext;
   // int imageTotal = 16;
    public String[] mThumbIds;
    private String[] mThumbNames;
    private static LayoutInflater mLayoutInflater=null;

    public ViewImageAdapter(Context c, String[] list) {
        this.mContext = c;
        this.mThumbIds = list;

        mLayoutInflater = ( LayoutInflater )c.
                getSystemService(Context.LAYOUT_INFLATER_SERVICE);
    }

    public int getCount() {
        return mThumbIds.length;
    }

    @Override
    public String getItem(int position) {
        return mThumbIds[position];
    }

    public long getItemId(int position) {
        return 0;
    }

    public View getView(int position, View convertView, ViewGroup parent) {
        View retval = LayoutInflater.from(parent.getContext()).inflate(R.layout.view_image, null);
        ImageView image_list_icon = (ImageView)retval.findViewById(R.id.os_images);

        String url = getItem(position);
        int length = url.length();
        if (length > 0) {
            Picasso.with(retval.getContext()).load(url).fit().centerCrop().into(image_list_icon);
        }
        return retval;
    }
}