//
//  GameViewController.m
//  AsteroidIdentifier
//
//  Created by Abdul Al-Shawa on 2016-04-23.
//  Copyright (c) 2016 Abdul Al-Shawa. All rights reserved.
//

#import "GameViewController.h"
#import "AsteroidCellView.h"

@implementation GameViewController {
	SCNScene *_scene;
	
	SCNNode *_textNode;
	
	SCNText *_titleText;
	SCNNode *_titleNode;
	
	SCNText *_subtitleText;
	SCNNode *_subtitleNode;
	
	SCNNode *_asteroid;
	
	NSDictionary *_unknownAsteroidsDictionary;
}

-(void)awakeFromNib
{
    [super awakeFromNib];

    // create a new scene
    SCNScene *scene = [SCNScene sceneNamed:@"art.scnassets/asteroid_vesta.scn"];

    // create and add a camera to the scene
    SCNNode *cameraNode = [SCNNode node];
    cameraNode.camera = [SCNCamera camera];
    [scene.rootNode addChildNode:cameraNode];
	
	//self.gameView.allowsCameraControl = YES;
	//self.gameView.autoenablesDefaultLighting = YES;
	
    // place the camera
    cameraNode.position = SCNVector3Make(0, 0, 15);
    
    // create and add a light to the scene
    SCNNode *lightNode = [SCNNode node];
    lightNode.light = [SCNLight light];
    lightNode.light.type = SCNLightTypeOmni;
    lightNode.position = SCNVector3Make(0, 10, 10);
    //[scene.rootNode addChildNode:lightNode];
    
    // create and add an ambient light to the scene
    SCNNode *ambientLightNode = [SCNNode node];
    ambientLightNode.light = [SCNLight light];
    ambientLightNode.light.type = SCNLightTypeAmbient;
    ambientLightNode.light.color = [NSColor darkGrayColor];
    [scene.rootNode addChildNode:ambientLightNode];
	
    // retrieve the ship node
    _asteroid = [scene.rootNode childNodeWithName:@"asteroid_vesta" recursively:YES];

    // animate the 3d object
    CABasicAnimation *animation = [CABasicAnimation animationWithKeyPath:@"rotation"];
    animation.toValue = [NSValue valueWithSCNVector4:SCNVector4Make(0, 1, 0, M_PI*2)];
    animation.duration = 10;
    animation.repeatCount = MAXFLOAT; //repeat forever
    [_asteroid addAnimation:animation forKey:nil];

	
    // set the scene to the view
    self.gameView.scene = scene;
    
    // allows the user to manipulate the camera
//    self.gameView.allowsCameraControl = YES;
	
    // show statistics such as fps and timing information
    self.gameView.showsStatistics = YES;
    
    // configure the view
    self.gameView.backgroundColor = [NSColor blackColor];
	
	_scene = scene;

	[self initGameViewTitles];
	
	dispatch_async(dispatch_get_global_queue(DISPATCH_QUEUE_PRIORITY_DEFAULT, 0), ^{
		// Retreieve asteroid data from PropertyList
		_unknownAsteroidsDictionary = [NSDictionary dictionaryWithContentsOfFile:[[NSBundle mainBundle] pathForResource:@"PresetUnknownAsteroids" ofType:@"plist"]];
		
		dispatch_async(dispatch_get_main_queue(), ^{
			[self.asteroidTableView reloadData];
		});
	});
}

-(void)viewWillAppear
{
	[super viewWillAppear];
	
//	dispatch_after(dispatch_time(DISPATCH_TIME_NOW, (int64_t)(5 * NSEC_PER_SEC)), dispatch_get_main_queue(), ^{
//		[self updateTitleWithString:@"YAY!"];
//		[self updateSubtitleWithString:@"WOOT!\nWOOT!!"];
//	});
}

- (void)initGameViewTitles
{
	_textNode = [SCNNode node];
	_textNode.position = SCNVector3Make(180, 200, -10);
	
	[_asteroid addChildNode:_textNode];
	
	// Build the title node  - - -
	_titleNode = [SCNNode node];
	
	SCNText *titleText = [SCNText textWithString:@"Asteroid 117" extrusionDepth:10.f];
	_titleNode.geometry = titleText;
	titleText.flatness = .4f;
	titleText.chamferRadius = 1.f;
	titleText.font = [NSFont fontWithName:@"Myriad Set" size:48] ?: [NSFont fontWithName:@"Avenir Medium" size:48];
	
	NSLayoutManager *layoutManager = [[NSLayoutManager alloc] init];
	CGFloat leading = [layoutManager defaultLineHeightForFont:titleText.font];
	CGFloat descender = titleText.font.descender;
	NSUInteger newlineCount = [[titleText.string componentsSeparatedByCharactersInSet:[NSCharacterSet newlineCharacterSet]] count];
	_titleNode.pivot = CATransform3DMakeTranslation(0, -descender + newlineCount * leading, 0);
	
	SCNMaterial *frontMaterial = [SCNMaterial material];
	SCNMaterial *sideMaterial = [SCNMaterial material];
	
	frontMaterial.emission.contents = [NSColor darkGrayColor];
	frontMaterial.diffuse.contents = [NSColor colorWithDeviceRed:115/255.0 green:170/255.0 blue:230/255.0 alpha:1];
	sideMaterial.diffuse.contents = [NSColor lightGrayColor];
	_titleNode.geometry.materials = @[frontMaterial, frontMaterial, sideMaterial, frontMaterial, frontMaterial];
	
	[_textNode addChildNode:_titleNode];
	
	_titleText = titleText;
	
	
	// Build the subtitle node - - -
	_subtitleNode = [SCNNode node];
	
	SCNText *subtitleText = [SCNText textWithString:@"Class A :D\nClass B :(" extrusionDepth:2.f];
	
	_subtitleNode.geometry = subtitleText;
	subtitleText.flatness = .4f;
	subtitleText.chamferRadius = 0.f;
	subtitleText.font = [NSFont fontWithName:@"Myriad Set" size:38] ?: [NSFont fontWithName:@"Avenir Medium" size:38];
	
	NSLayoutManager *layoutManager2 = [[NSLayoutManager alloc] init];
	CGFloat leading2 = [layoutManager2 defaultLineHeightForFont:subtitleText.font];
	CGFloat descender2 = subtitleText.font.descender;
	NSUInteger newlineCount2 = [[subtitleText.string componentsSeparatedByCharactersInSet:[NSCharacterSet newlineCharacterSet]] count];
	_subtitleNode.pivot = CATransform3DMakeTranslation(0, -descender2 + newlineCount2 * leading2, 0);
	
	SCNMaterial *frontMaterial2 = [SCNMaterial material];
	SCNMaterial *sideMaterial2 = [SCNMaterial material];
	
	frontMaterial.emission.contents = [NSColor darkGrayColor];
	frontMaterial.diffuse.contents = [NSColor colorWithDeviceRed:115/255.0 green:170/255.0 blue:230/255.0 alpha:1];
	sideMaterial.diffuse.contents = [NSColor lightGrayColor];
	_subtitleNode.geometry.materials = @[frontMaterial2, frontMaterial2, sideMaterial2, frontMaterial2, frontMaterial2];
	
	_subtitleNode.position = SCNVector3Make(_titleNode.position.x, _titleNode.position.y - 55.f, _titleNode.position.z); // TODO: Use bounding box API on geo.
	
	[_textNode addChildNode:_subtitleNode];
	
	_subtitleText = subtitleText;
	
	
	[_textNode addChildNode:_titleNode];
	[_textNode addChildNode:_subtitleNode];
	
	
	// Fade In of the two title nodes at different rates
	_titleNode.opacity = 0;
	_subtitleNode.opacity = 0;
	[SCNTransaction begin];
	[SCNTransaction setAnimationDuration:2.0];
	{
		_titleNode.opacity = 1;
	}
	[SCNTransaction setAnimationDuration:3.5f];
	{
		_subtitleNode.opacity = 1;
	}
	[SCNTransaction commit];
}

- (void)updateTitleWithString:(NSString *)title
{
	_titleText.string = title;
}

- (void)updateSubtitleWithString:(NSString *)subtitle
{
	_subtitleText.string = subtitle;
}

@end
