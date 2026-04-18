clc;
clear;
close all;

%% -------- PATHS --------
base_folder = "C:\Users\Lenovo\Favorites\Juili Gulhane\COEP\Academics\2nd Sem\Auto Intelligence\Assignments\DDD\DDD Database\Driver Drowsiness Dataset (DDD)";
output_video = "C:\Users\Lenovo\Favorites\Juili Gulhane\COEP\Academics\2nd Sem\Auto Intelligence\Assignments\DDD\output_video.avi";

%% -------- USER CONTROL --------
person = 'A';
start_img = 100;
end_img = 160;   % keep small for smooth video

EAR_THRESH = 0.26;
MAR_THRESH = 0.7;
TEMPORAL_WINDOW = 5;
DROWSY_TRIGGER = 3;

%% -------- BUILD SEQUENCE (REAL VIDEO STYLE) --------
image_list = [];
label_list = [];

% First DROWSY sequence
for i = start_img:end_img
    file = sprintf('%c%04d.png', upper(person), i);
    path = fullfile(base_folder, "Drowsy", file);
    if isfile(path)
        image_list = [image_list; string(path)];
        label_list = [label_list; 1];
    end
end

% Then NON-DROWSY sequence
for i = start_img:end_img
    file = sprintf('%c%04d.png', lower(person), i);
    path = fullfile(base_folder, "Non Drowsy", file);
    if isfile(path)
        image_list = [image_list; string(path)];
        label_list = [label_list; 0];
    end
end

disp("Total frames: " + length(image_list));

%% -------- VIDEO --------
v = VideoWriter(output_video, 'Motion JPEG AVI');
v.FrameRate = 20;   % 🔥 faster video
open(v);

%% -------- DETECTORS --------
faceDetector = vision.CascadeObjectDetector();
eyeDetector = vision.CascadeObjectDetector('EyePairBig');
mouthDetector = vision.CascadeObjectDetector('Mouth','MergeThreshold',8);

%% -------- METRICS --------
correct = 0;
total = 0;
actual_vals = [];
predicted_vals = [];

history = zeros(1, TEMPORAL_WINDOW);

figure;

%% -------- MAIN LOOP --------
for i = 1:length(image_list)
    disp(i);
    img_path = image_list(i);
    actual = label_list(i);

    frame = imread(img_path);
    frame = imresize(frame,[480 640]);

    bbox = step(faceDetector,frame);

    EAR = 0; MAR = 0; instant_drowsy = 0;

    if ~isempty(bbox)

        frame = insertShape(frame,"Rectangle",bbox,"Color","green");

        faceROI = imcrop(frame,bbox(1,:));

        % ---- EYE ----
        eyeBbox = step(eyeDetector,faceROI);
        if ~isempty(eyeBbox)
            eb = eyeBbox(1,:);
            EAR = eb(4)/eb(3);

            eb(1)=eb(1)+bbox(1);
            eb(2)=eb(2)+bbox(2);

            frame = insertShape(frame,"Rectangle",eb,"Color","yellow","LineWidth",3);
        end

        % ---- MOUTH ----
        mouthBbox = step(mouthDetector,faceROI);
        if ~isempty(mouthBbox)
            mb = mouthBbox(1,:);
            MAR = mb(4)/mb(3);

            mb(1)=mb(1)+bbox(1);
            mb(2)=mb(2)+bbox(2);

            frame = insertShape(frame,"Rectangle",mb,"Color","cyan","LineWidth",3);
        end

        if EAR < EAR_THRESH || MAR > MAR_THRESH
            instant_drowsy = 1;
        end
    end

    % ---- TEMPORAL ----
    history = [history(2:end) instant_drowsy];

    if sum(history) >= DROWSY_TRIGGER
        status = "Drowsy";
        predicted = 1;
    else
        status = "Non-Drowsy";
        predicted = 0;
    end

    % ---- METRICS ----
    actual_vals = [actual_vals actual];
    predicted_vals = [predicted_vals predicted];

    if predicted == actual
        correct = correct + 1;
    end
    total = total + 1;
    acc = (correct/total)*100;

    % ---- DISPLAY ----
    frame = insertText(frame,[10 10],sprintf("EAR: %.2f",EAR),"TextColor","white","BoxColor","black");
    frame = insertText(frame,[10 40],sprintf("MAR: %.2f",MAR),"TextColor","white","BoxColor","black");
    frame = insertText(frame,[10 420],"Status: "+status,"TextColor","white","BoxColor","red");

    imshow(frame);
    drawnow;
pause(0.03);   % ~30 FPS visual playback

    writeVideo(v,frame);

end

close(v);
close all;

fprintf("Final Accuracy: %.2f%%\n", acc);

figure('Name','Driver Monitoring','NumberTitle','off');
confusionchart(actual_vals,predicted_vals);
title("Confusion Matrix");