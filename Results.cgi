#!c:/Perl/bin/perl.exe
use CGI qw/:standard/;
#   	  	  
#    Name:	  Maeda Hanafi
#  	 Course:	   543
#  	 Assignment:	   #3
#  
print "Content-type: text/html\n\n";
$query = new CGI;
print $query->start_html('My survey results');
print $query->body({bgcolor=>'#9999FF'});
print $query->center;

open(QFILE, 'Results.txt');
@results = <QFILE>;
close(QFILE);

print $query->start_table({-style=>"border:2px solid blue"});

#extract header format
$numresults=$results[1];
@header = split(/&/, $numresults);
$numquestion = @header ;
for($i=0;$i<$numquestion;$i++){
	print $query->td({-style=>"border:2px solid purple"}, "$header[$i]");
}

#extract results
$filesize = @results;

#reverse arary and get the first occurence of the array(user final answers)
$currnum = $numquestion-1;
for($i=$filesize-1; $i>=2 ;$i--){
	@extract = split(/&/, $results[$i]);
	if($extract[0]==$currnum){
		$dispsize = @disparr;
		@disparr[$dispsize]= $extract[1];
		$currnum--;
		if($currnum==0){
			$currnum = $numquestion-1;
		}
	}
}


$dispsize = @disparr;

#indicate a new row
$ctr = -1;
my @rows;
my $row = '';
$rownum = 0;

for($i=$dispsize;$i>=0;$i--){
	#add a td
	$row .= td({-style=>"border:2px solid blue"},$disparr[$i]);
	$ctr++;
	if($ctr%($numquestion-1)==0){
		#a new row
		push @rows, $row;
		#set for next row
		$row = '';
		$rownum++;
		$row .= td({-style=>"border:2px solid blue"}, "$rownum");
		$ctr=0;
		
	}
		
}
print $query->Tr([@rows]);

print $query->end_table();

print $query->end_html;