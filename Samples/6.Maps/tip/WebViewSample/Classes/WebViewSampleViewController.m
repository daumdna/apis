//
//  WebViewSampleViewController.m
//  WebViewSample
//
//  Created by 승철 이 on 12. 5. 22..
//  Copyright 다음 2012. All rights reserved.
//

#import "WebViewSampleViewController.h"

@implementation WebViewSampleViewController

@synthesize webView;

- (void)viewDidLoad {
    [super viewDidLoad];

	NSURL *url = [[NSURL alloc] initWithString:@"http://dna.daum.net/examples/maps/maps3/mobile_simple.html"];
    [webView loadRequest:[NSURLRequest requestWithURL:url]];
}


/*
// Override to allow orientations other than the default portrait orientation.
- (BOOL)shouldAutorotateToInterfaceOrientation:(UIInterfaceOrientation)interfaceOrientation {
    // Return YES for supported orientations
    return (interfaceOrientation == UIInterfaceOrientationPortrait);
}
*/

- (void)didReceiveMemoryWarning {
	// Releases the view if it doesn't have a superview.
    [super didReceiveMemoryWarning];
	
	// Release any cached data, images, etc that aren't in use.
}

- (void)viewDidUnload {
	// Release any retained subviews of the main view.
	// e.g. self.myOutlet = nil;
}


- (void)dealloc {
    [super dealloc];
}

@end
