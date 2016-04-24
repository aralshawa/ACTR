//
//  GameViewController.m
//  AsteroidIdentifier
//
//  Created by Abdul Al-Shawa on 2016-04-23.
//  Copyright (c) 2016 Abdul Al-Shawa. All rights reserved.
//

#import "GameViewController.h"
#import "AsteroidCellView.h"

#import <QuartzCore/QuartzCore.h>
#import <CorePlot/CorePlot.h>

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
    animation.toValue = [NSValue valueWithSCNVector4:SCNVector4Make(0, 1, 0, M_PI * 2)];
    animation.duration = 24;
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
	
	// NSTableView
//	self.asteroidTableView.selectionHighlightStyle = NSTableViewSelectionHighlightStyleNone;
	
	dispatch_async(dispatch_get_global_queue(DISPATCH_QUEUE_PRIORITY_DEFAULT, 0), ^{
		// Retreieve asteroid data from PropertyList
		_unknownAsteroidsDictionary = [NSDictionary dictionaryWithContentsOfFile:[[NSBundle mainBundle] pathForResource:@"PresetUnknownAsteroids" ofType:@"plist"]];
		
		dispatch_async(dispatch_get_main_queue(), ^{
			[self.asteroidTableView reloadData];
		});
	});
}

- (void)initGameViewTitles
{
	_textNode = [SCNNode node];
	_textNode.position = SCNVector3Make(170, 200, -15);
	
	[_asteroid.parentNode addChildNode:_textNode];
	
	// Build the title node  - - -
	_titleNode = [SCNNode node];
	
	SCNText *titleText = [SCNText textWithString:@"Asteroid 117" extrusionDepth:10.f];
	_titleNode.geometry = titleText;
	titleText.flatness = .4f;
	titleText.chamferRadius = 1.f;
	titleText.font = [NSFont fontWithName:@"Myriad Set" size:38] ?: [NSFont fontWithName:@"Avenir Medium" size:38];
	
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
	subtitleText.font = [NSFont fontWithName:@"Myriad Set" size:28] ?: [NSFont fontWithName:@"Avenir Medium" size:28];
	
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

#pragma mark - <NSTableViewDelegate, NSTableViewDataSource>

- (NSInteger)numberOfRowsInTableView:(NSTableView *)tableView
{
	return [_unknownAsteroidsDictionary count];
}

//- (CGFloat)tableView:(NSTableView *)tableView heightOfRow:(NSInteger)row
//{
//	
//}

- (NSView *)tableView:(NSTableView *)tableView viewForTableColumn:(NSTableColumn *)tableColumn row:(NSInteger)row
{
	AsteroidCellView *cellView = [tableView makeViewWithIdentifier:@"AsteroidCellView" owner:self];
	
	NSString *entryKey = [_unknownAsteroidsDictionary allKeys][row]; // TODO: This is fragile and not correct.
	
	NSArray *splitKey = [entryKey componentsSeparatedByString:@"_"];
	NSString *entryID = splitKey[0];
	NSString *entryName = splitKey[1];
	
	cellView.asteroidIDLabel.stringValue = entryID;
	cellView.asteroidNameLabel.stringValue = entryName;
	cellView.asteroidImageView.image = [NSImage imageNamed:@"asteroid_icon"];
	
	return cellView;
}

- (BOOL)tableView:(NSTableView *)tableView shouldSelectRow:(NSInteger)row
{
	if (tableView.selectedRow != row) {
		NSString *entryKey = [_unknownAsteroidsDictionary allKeys][row]; // TODO: This is fragile and not correct.
		NSArray *splitKey = [entryKey componentsSeparatedByString:@"_"];
		NSString *entryID = splitKey[0];
		NSString *entryName = splitKey[1];
		NSString *entrySpectrum = [[_unknownAsteroidsDictionary objectForKey:entryKey] stringByTrimmingCharactersInSet:[NSCharacterSet characterSetWithCharactersInString:@"[]"]];
		NSArray *spectrumEntries = [entrySpectrum componentsSeparatedByString:@","];
		
		// Update the titles to show progress
		dispatch_async(dispatch_get_main_queue(), ^{
			[self updateTitleWithString:[NSString stringWithFormat:@"#%@ - %@", entryID, entryName]];
			[self updateSubtitleWithString:@"Evaluating..."];
		});
		
		// Dispatch call python scripts to evaluate confidence scores based on known data
		dispatch_async(dispatch_get_global_queue(DISPATCH_QUEUE_PRIORITY_DEFAULT, 0), ^{
			// TODO: Bring these paths up to a prepros macro
			NSString *path = @"/Library/Frameworks/Python.framework/Versions/3.5/bin/python3";
			NSArray *args = [[NSArray arrayWithObjects:@"/Users/AbdulAl-shawa/Documents/Developer/spaceapps2016/parser.py", nil] arrayByAddingObjectsFromArray:spectrumEntries];
			NSTask *pyOp = [[NSTask alloc] init];
			pyOp.launchPath = path;
			
			NSPipe *outputPipe = [NSPipe pipe];
			[pyOp setStandardOutput:outputPipe];
			
			pyOp.arguments = args;
			[pyOp launch];
			[pyOp waitUntilExit];
			
			NSData *outputData = [[outputPipe fileHandleForReading] readDataToEndOfFile];
			NSString *outputString = [[NSString alloc] initWithData:outputData encoding:NSUTF8StringEncoding];
			
			NSArray *alternatingClassVsConfScores = [outputString componentsSeparatedByString:@","];
			
			NSMutableArray *combined = [NSMutableArray array];
			for (NSUInteger i = 0; i < alternatingClassVsConfScores.count; i+= 2) {
				[combined addObject: @{@"type" : alternatingClassVsConfScores[i], @"conf": [NSNumber numberWithFloat:[alternatingClassVsConfScores[i + 1] floatValue]]}];
			}
			
			[combined sortUsingDescriptors:@[[NSSortDescriptor sortDescriptorWithKey:@"conf" ascending:NO]]];
			
			dispatch_async(dispatch_get_main_queue(), ^{
				[self updateSubtitleWithString:[NSString stringWithFormat:@"Class %@  High Conf\nClass %@  Runner Up", combined[0][@"type"], combined[1][@"type"]]];
			});
		});
		
		return YES;
	} else {
		return NO;
	}
}

@end
