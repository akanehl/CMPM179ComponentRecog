using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CameraScript : MonoBehaviour
{
    static WebCamTexture CameraFeed;


    // Start is called before the first frame update
    void Start()
    {
        if(CameraFeed == null)
        {
            CameraFeed = new WebCamTexture();
        }

        GetComponent<Renderer>().material.mainTexture = CameraFeed;

        if(!CameraFeed.isPlaying)
        {
            CameraFeed.Play();
        }
    }

}
