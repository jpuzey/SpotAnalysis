// VESSEL_ANALYSIS

requires("1.47g");
base = getTitle();
directory = getDirectory("image");

do {
	// Prompt user to select image boundaries
	setTool(0);
	beep();
	waitForUser("Define image", "Select image boundaries, then click OK.");
} while(selectionType() == -1);

// Crop image to selected boundaries & save
run("Crop");
run("Select None");
saveAs("Tiff", directory + "Cropped-" + base);

run("Invert");

/**********************************************
*     Create a binary image of vasculature    *
**********************************************/

setBatchMode(true);
run("Duplicate...", "title=[" + "Cropped-" + base + "]");
rename("Binary-" + base);
binary = getTitle();

// Preserve green channel; discard red and blue channels
//run("Split Channels");
//selectWindow(binary + " (blue)");
//close();
//selectWindow(binary + " (red)");
//close();
//selectWindow(binary + " (green)");


// Equalize histogram, apply Laplacian of Gaussian filter & auto-threshold
run("Enhance Contrast...", "saturated=0.4 equalize");
run("Mexican Hat Filter", "radius=5");
run("Auto Threshold", "method=Shanbhag");



// Fill in holes
//run("Remove Outliers...", "radius=1 threshold=10 which=Dark");


// Remove background noise
for (i = 0; i < 2; i++)
	run("Remove Outliers...", "radius=3 threshold=10 which=Bright");
for (i = 0; i < 10; i++)
	run("Despeckle");

//run("Particle Remover", "Size=0-100");



saveAs("Tiff", directory + binary);


close("Cropped-" + base);
setBatchMode(false);

/*************************************
*     Perform vessel measurements    *
*************************************/

do {
	run("Particle Remover", "size=0-200 circularity=0-1");

	saveAs("Tiff", directory + binary + "vein");
	vein = getTitle();

	selectWindow(vein);

	// Prompt user to select image operation
	items = newArray("Vascular Density Metrics", "Diameter Measurements");
	Dialog.create("Image Opertions");
	Dialog.addRadioButtonGroup("Select measurement to perform:", items, 1, 3, "Vascular Density Metrics");
	Dialog.show();

	// Execute corresponding program
	choice = Dialog.getRadioButton();
	setBatchMode(true);

	if (choice == "Diameter Measurements") {
		run("Duplicate...", "title=[" + vein + "]");
		rename("Duplicate-" + vein);
		duplicate = getTitle();

		// Calculate EDM & colour pixels based on "Fire" look-up table
		run("Geometry to Distance Map", "threshold=1");
		processed = getTitle();

		// Skeletonize pre-EDM image
		selectWindow(duplicate);
		setOption("BlackBackground", true);
		run("Skeletonize");

		// Convert pixel values to 0 (black) or 1 (white)
		run("RGB Color");
		run("8-bit Color", "number=2");

		// Multiply pixels of both images to produce skeletonized image of coloured vessels
		imageCalculator("Multiply create 32-bit", duplicate, processed);
		run("Fire");
		intermediate = getTitle();

		// Double pixels values (radius values -> diameter values)
		imageCalculator("Add create 32-bit", intermediate, intermediate);

		// Final image produced; close previous images
		rename("EDM-" + base);
		result = getTitle();
		saveAs("Tiff", directory + result);

		close(duplicate);
		close(processed);
		close(intermediate);
		selectWindow(result);
		setBatchMode(false);
		run("Diameter Measurements");
	}

	else if (choice == "Vascular Density Metrics") {
		selectWindow(binary);
		saveAs("Tiff", directory + "VD" + binary);
		run("Vascular Density");
		open(binary);
	}
	else
		print("No operation was selected.");

	// Ask user to perform another measurement
	repeat = getBoolean("Would you like to perform another measurement?");

} while(repeat)
