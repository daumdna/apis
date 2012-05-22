//
//  WebViewSampleAppDelegate.h
//  WebViewSample
//
//  Created by 승철 이 on 12. 5. 22..
//  Copyright 다음 2012. All rights reserved.
//

#import <UIKit/UIKit.h>

@class WebViewSampleViewController;

@interface WebViewSampleAppDelegate : NSObject <UIApplicationDelegate> {
    UIWindow *window;
    WebViewSampleViewController *viewController;
}

@property (nonatomic, retain) IBOutlet UIWindow *window;
@property (nonatomic, retain) IBOutlet WebViewSampleViewController *viewController;

@end

