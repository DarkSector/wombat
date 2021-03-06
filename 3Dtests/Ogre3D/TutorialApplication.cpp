/*
-----------------------------------------------------------------------------
Filename:    TutorialApplication.cpp
-----------------------------------------------------------------------------
*/
#include "TutorialApplication.h"
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>

//-------------------------------------------------------------------------------------
TutorialApplication::TutorialApplication(char *i, char *o)
{
	currentAngle = 10;
	accumulatedTime = 0;
	imagecount = 0;
	inputfile = i;
	outputfolder = o;
	
	printf("inputfile: %s \n outputfolder: %s", inputfile,outputfolder);

	
	
}
//-------------------------------------------------------------------------------------
TutorialApplication::~TutorialApplication(void)
{
}

//-------------------------------------------------------------------------------------

void TutorialApplication::createCamera(void)
{
    mCamera = mSceneMgr->createCamera("playercam");
    mCamera->setPosition(200,0,0);
    mCamera->lookAt(10,0,0);
    mCamera->setNearClipDistance(5);
    mCameraMan = new OgreBites::SdkCameraMan(mCamera);

}

void TutorialApplication::createViewport(void)
{
	
	

}


void TutorialApplication::createScene(void)
{
    //create primary entity
    ent = mSceneMgr->createEntity("foo",inputfile);
    
    //this entity is for testing only
    //Ogre::Entity* ent2 = mSceneMgr->createEntity("Ogrehead2","ogrehead.mesh");
    
    //cretae node to which .mesh entity will be attached
    node = mSceneMgr->getRootSceneNode()->createChildSceneNode("Node1");
    node->setPosition(10,0,0);
    node->attachObject(ent);
    

    //Ogre::SceneNode* camnode = node->createChildSceneNode("Node2",Ogre::Vector3(80,0,0));
    //camnode->attachObject(ent2);
    //camnode->attachObject(cam1);
    //camnode->attachObject(mCamera);
    
    mSceneMgr->setAmbientLight(Ogre::ColourValue(1,1,1));
    
    Ogre::Light* light = mSceneMgr->createLight("mainlight");
    light->setDiffuseColour(Ogre::ColourValue::White);
    light->setPosition(10,100,0);
    mCamera->setAutoTracking(true, node);

}


bool TutorialApplication::frameRenderingQueued(const Ogre::FrameEvent& evt)
{
	char filename[100];
	if(mWindow->isClosed())	return false;

    if(mShutDown)
        return false;

	float time;

	time = evt.timeSinceLastFrame;
	
	accumulatedTime += time;
	
	
	//printf("Frame time = %f\n", time);
	
	//if (accumulatedTime > 0.5) {
		//accumulatedTime = 0;
		
		//printf("Inside yaw code\n");
		
		if (imagecount == 35)
			return false;
		//currentAngle == 0;
		
	    node->yaw(Ogre::Degree(currentAngle));
	    //currentAngle += 10.0;
	    
	    glPixelStorei(GL_PACK_ALIGNMENT,1);
	    
	    sprintf(filename,"%s/file-%d.png", outputfolder, imagecount);
	    imagecount++;
	    mWindow->writeContentsToFile(filename);
	    printf("%s\n",filename);
	//}
	
	//Need to capture/update each device
    mKeyboard->capture();
    mMouse->capture();
        
	//printf("Time since last frame = %f", time);
	
	
	return true;
}


#if OGRE_PLATFORM == OGRE_PLATFORM_WIN32
#define WIN32_LEAN_AND_MEAN
#include "windows.h"
#endif

#ifdef __cplusplus
extern "C" {
#endif

#if OGRE_PLATFORM == OGRE_PLATFORM_WIN32
    INT WINAPI WinMain( HINSTANCE hInst, HINSTANCE, LPSTR strCmdLine, INT )
#else
    int main(int argc, char *argv[])
#endif
    {
        // Create application object
        
        
        if (argc !=3)
        {
            printf("Usage: %s [input] [output] \n\n", argv[0]);
            exit(0);
        }
        
        struct stat buf;
        int ret;
        printf("Checking if output path exists...\n");
        ret = stat(argv[2],&buf);
        //printf("%d %d\n", ret, buf.st_mtime);
        if (ret== -1)
        {
            printf("Path does not exist: %s \nCowardly refusing to run the program \n", argv[2]);
            exit(0);
        }
        
        
        
        TutorialApplication app(argv[1],argv[2]);
        
        
        try {
            app.go();
        } catch( Ogre::Exception& e ) {
#if OGRE_PLATFORM == OGRE_PLATFORM_WIN32
            MessageBox( NULL, e.getFullDescription().c_str(), "An exception has occured!", MB_OK | MB_ICONERROR | MB_TASKMODAL);
#else
            std::cerr << "An exception has occured: " <<
                e.getFullDescription().c_str() << std::endl;
#endif
        }

        return 0;
    }

#ifdef __cplusplus
}
#endif
