clc;
clear;
close all;

%% -------- PATHS --------
drowsy_folder = "C:\Users\Lenovo\Favorites\Juili Gulhane\COEP\Academics\2nd Sem\Auto Intelligence\Assignments\DDD\DDD Database\Driver Drowsiness Dataset (DDD)\Drowsy";
non_drowsy_folder = "C:\Users\Lenovo\Favorites\Juili Gulhane\COEP\Academics\2nd Sem\Auto Intelligence\Assignments\DDD\DDD Database\Driver Drowsiness Dataset (DDD)\Non Drowsy";

output_video = "C:\Users\Lenovo\Favorites\Juili Gulhane\COEP\Academics\2nd Sem\Auto Intelligence\Assignments\DDD\output_video.avi";

%% -------- LOAD IMAGES --------
drowsy_imgs = dir(fullfile(drowsy_folder, "*.png"));
non_drowsy_imgs = dir(fullfile(non_drowsy_folder, "*.png"));

all_imgs = [drowsy_imgs; non_drowsy_imgs];

disp("Total images found: " + length(all_imgs));

if isempty(all_imgs)
    error("❌ No images found!");
end

%% -------- LIMIT TO 100 --------
max_images = 100;
all_imgs = all_imgs(1:min(max_images, length(all_imgs)));

disp("Using images: " + length(all_imgs));

%% -------- VIDEO SETUP --------
v = VideoWriter(output_video);
v.FrameRate = 10;
open(v);

%% -------- DETECTORS --------
faceDetector = vision.CascadeObjectDetector();
eyeDetector = vision.CascadeObjectDetector('EyePairBig');
mouthDetector = vision.CascadeObjectDetector('Mouth');

%% -------- ACCURACY --------
correct = 0;
total = 0;

%% -------- FIGURE --------
hFig = figure;

%% -------- MAIN LOOP --------
for i = 1:length(all_imgs)

    img_path = fullfile(all_imgs(i).folder, all_imgs(i).name);
    frame = imread(img_path);

    frame = imresize(frame, [480 640]);

    % ---- GROUND TRUTH ----
    if contains(img_path, "Drowsy")
        actual = 1;
    else
        actual = 0;
    end

    % ---- DETECTION ----
    bbox = step(faceDetector, frame);

    status = "Non-Drowsy";
    EAR = 0; MAR = 0; head = "Forward";

    if ~isempty(bbox)

        frame = insertShape(frame, "Rectangle", bbox, "Color", "green");

        faceROI = imcrop(frame, bbox(1,:));

        % ---- EYE ----
        eyeBbox = step(eyeDetector, faceROI);
        if ~isempty(eyeBbox)
            eye_h = eyeBbox(1,4);
            eye_w = eyeBbox(1,3);
            EAR = eye_h / eye_w;

            if EAR < 0.25
                status = "Drowsy";
            end
        end

        % ---- MOUTH ----
        mouthBbox = step(mouthDetector, faceROI);
        if ~isempty(mouthBbox)
            mouth_h = mouthBbox(1,4);
            mouth_w = mouthBbox(1,3);
            MAR = mouth_h / mouth_w;

            if MAR > 0.6
                status = "Yawning";
            end
        end

        % ---- HEAD POSE ----
        face_x = bbox(1,1);

        if face_x < 150
            head = "Left";
            status = "Distracted";
        elseif face_x > 350
            head = "Right";
            status = "Distracted";
        else
            head = "Forward";
        end
    else
        status = "No Face";
    end

    % ---- PREDICTION ----
    if status == "Drowsy" || status == "Yawning" || status == "Distracted"
        predicted = 1;
    else
        predicted = 0;
    end

    % ---- ACCURACY UPDATE ----
    if predicted == actual
        correct = correct + 1;
    end
    total = total + 1;

    accuracy = (correct / total) * 100;

    % ---- OVERLAY TEXT ----
    frame = insertText(frame, [10 10], sprintf("EAR: %.2f", EAR), ...
        "FontSize", 14, "BoxColor", "black", "TextColor", "white");

    frame = insertText(frame, [10 40], sprintf("MAR: %.2f", MAR), ...
        "FontSize", 14, "BoxColor", "black", "TextColor", "white");

    frame = insertText(frame, [10 70], "Head: " + head, ...
        "FontSize", 14, "BoxColor", "black", "TextColor", "white");

    frame = insertText(frame, [10 420], "Status: " + status, ...
        "FontSize", 18, "BoxColor", "red", "TextColor", "white");

    frame = insertText(frame, [400 10], ...
        sprintf("Accuracy: %.2f%%", accuracy), ...
        "FontSize", 14, "BoxColor", "black", "TextColor", "white");

    % ---- DISPLAY ----
    imshow(frame);
    drawnow;

    % ---- WRITE VIDEO ----
    writeVideo(v, frame);

end

%% -------- CLEANUP --------
close(v);
close(hFig);

final_accuracy = (correct / total) * 100;
fprintf("✅ Final Accuracy: %.2f%%\n", final_accuracy);