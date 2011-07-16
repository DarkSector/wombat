/*
-----------------------------------------------------------------------------
Filename:    TutorialApplication.h
-----------------------------------------------------------------------------

*/
#ifndef __TutorialApplication_h_
#define __TutorialApplication_h_

#include "BaseApplication.h"
#include "GL/gl.h"
#include "stdio.h"

class TutorialApplication : public BaseApplication
{
public:
    TutorialApplication(void);
    virtual ~TutorialApplication(void);
    
protected:
    virtual void createScene(void);
    virtual void createCamera(void);
    virtual void createViewport(void);
    
    bool mouseMoved( const OIS::MouseEvent &arg ) {};
    bool mousePressed( const OIS::MouseEvent &arg, OIS::MouseButtonID id ) {};
    bool mouseReleased( const OIS::MouseEvent &arg, OIS::MouseButtonID id ) {};
    
    
    //virtual void writeContentsToFile(const String & filename);
    bool frameRenderingQueued(const Ogre::FrameEvent& evt);
	bool frameEnded(const Ogre::FrameEvent& evt)
	{
		//updateStats();
		return true; 
	};
	int imagecount;
	
	Ogre::Entity *ent;
	
	float currentAngle;
	float accumulatedTime;
	
	Ogre::SceneNode *node;
};

#endif // #ifndef __TutorialApplication_h_
