using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CameraScript : MonoBehaviour
{
    static WebCamTexture CameraFeed;

    public string filePath;
    int fileNum;


    // Start is called before the first frame update
    void Start()
    {

        fileNum = 0;

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

    void Update()
    {
      if( Input.GetKeyDown(KeyCode.S))
        {
            fileNum++;
            string returnedVal = constFilePath();
            ScreenCapture.CaptureScreenshot(returnedVal, 1);
        }
    }

    string constFilePath()
    {
        string retVal;
        retVal = filePath + "\\screencapture" + fileNum.ToString() + ".png";

        return retVal;
    }

}
