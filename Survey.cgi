#!c:/Perl/bin/perl.exe
use CGI qw/:standard/;
#   	  	  
#    Name:	  Maeda Hanafi
#  	 Course:	   543
#  	 Assignment:	   #3
#   
print "Content-type: text/html\n\n";

$query = new CGI;
print $query->start_html('My survey program');
print $query->body({bgcolor=>'#9999FF'});

#read which question
open(QFILE, 'Results.txt');
@results= <QFILE>;
#get question num
$index=$results[0];
close(QFILE);

# check if prev button was clicked
if($query->param("prev")){
	$index=$index-2;
	if($index<0){
		$index=0;
	}
}

#start of form
print $query->startform(-name=>'myform',
						-method=>'POST',
						-action=>'Survey.cgi');

						
#read question text file
open(MYFILE, 'Questions.txt');
@questionsize = <MYFILE>;
close (MYFILE);
$qsize = @questionsize;

$perdone = int(100*($index/$qsize));
$donewidth =  $perdone;
$notdonewidth =( 100- $donewidth);

#draw bar
$style1 = "Color: lightblue;background-color:lightblue;height:20px;width:".$notdonewidth."px;float:right;";
$style2 = "Color: black; background-color:blue;height:20px;width:".$donewidth."px; float:right;";
print $query->div ({-id=>'progressbar1', -align=>right, -style=>$style1 },'|');
print $query->div ({-id=>'progressbar', -align=>right, -style=>$style2 },"$perdone%");

if($qsize>$index){
	#draw next and prev button
	print $query->br;
		print $query->p({-align=>right},
		 $query->submit(-name=>"prev",-value=>'Prev'),
		 $query->submit(-value=>'Next')
		);
}

#if the last question indicate end of survey
if($index==$qsize){
	#$index=0;
	print $query->center;
	print $query->p("Thank you for your input.");
}
else{
	#read question text file
	open(MYFILE, 'Questions.txt');
	print $query->center;
	#print the current question
	$questionum = 0;
	while(<MYFILE>){
		chomp;
		($text, $questiontype, $radioinfo) = split(/<->/, $_);
		#display if it is reight question 	 
		if($questionnum==$index){
			$disp = $questionnum+1;
			print $query->p("$disp. $text");
			print $query->br;
			
			if($questiontype =~ "radio"){			
				@radiostuff = split('<\+>',$radioinfo);
				print $query->radio_group(
					-name=>'radio',
					-values=>\@radiostuff);
			}elsif($questiontype =~ "textarea"){
				print $query->textarea(
					-name=>"TEXT_AREA",
					-default=>"Enter here",
					-size=>'7',
					-rows=>'10',
					-columns=>'50');
				print $query->br;
			}elsif($questiontype =~ "text"){
				print $query->textfield(
					-name=>"TEXT_FIELD",
					-default=>"Enter here",
					-size=>'12');
				print $query->br;
			}
		}
		
		$questionnum++;
	}


	close (MYFILE);

} 

print $query->endform;

#extract result if a previous question was answered
	$yourText = $query->param("TEXT_AREA");
	$yourText1 = $query->param("TEXT_FIELD");
	$yourradio2 = $query->param('radio');
	
#set result file
$results[1] = "#&Q1&Q2&Q3&Q4&Q5&Q6\n";

#form the result

#append new result to file if next button clicked
$size = @results;

	# check if prev button was clicked
	if($query->param("prev")){
		$dispi=$index+1;
	}else{
		$dispi = $index;
	}
	$printi = $size+1;
	#append answer to file along with question number. 
	#0& indicates a new survey
	if($query->param('TEXT_AREA')){$results[$printi] = "$dispi&$yourText\n";}
	elsif($query->param('TEXT_FIELD')){$results[$printi] = "$dispi&$yourText1\n";}
	elsif($query->param('radio')){$results[$printi] = "$dispi&$yourradio2\n";}
	else{$results[$printi] = "$dispi&\n";}
	$results[$printi]=~ s/\R//g;
	$results[$printi]=~s/^\s+//g;

$results[$printi] = $results[$printi]."\n";

#set next page
$index=$index+1;
if($index>$questionnum){
	$index=0;
}
$results[0] = "$index\n";

#write to results file
open (FRESULT, '>Results.txt'); 
	print FRESULT @results;
close(FRESULT);

print $query->end_html;