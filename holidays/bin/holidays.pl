#!/usr/bin/perl -w
 
BEGIN { eval { require bytes; }; }
use strict;
 
use Date::Calendar::Profiles qw( $Profiles );
use Date::Calendar::Year;
use Date::Calc::Object qw(:ALL);
 
sub print_holidays
{
    my($year_start) = shift_year(\@_);
    my($year_end) = shift_year(\@_);
    my($prof) = shift;
    my($times) = shift;
    my($j,$year_curr,$full,$half,$last,$i,$date,$year,$month,$day,@labels,$dow,$holiday);
    my $return;
 
    die "No such calendar profile '$prof'"
        unless (exists $Profiles->{$prof});
 
	for ( $j = $year_start; $j <= $year_end; $j++ )
	{
		    $year_curr = Date::Calendar::Year->new( $j, $Profiles->{$prof} );
 
		    $full = $year_curr->vec_full();
		    $half = $year_curr->vec_half();
		    $last = $year_curr->val_days();
 
		    Language(1);
		    Date::Calc->date_format(0);
 
		    for ( $i = 0; $i < $last; $i++ )
		    {
		    	$date = $year_curr->index2date($i);
		    	@labels = $year_curr->labels($date);
		    	($year,$month,$day) = $date->date();
		        if (@labels > 1)
		        {
		            $dow = substr(shift(@labels),0,3);
		            # we skip saturdays and sundays!
		            next if ( $dow eq "Sat" || $dow eq "Sun" );
		            # we only want "full" and "half" holidays!
		            $holiday = $full->contains($i) ? "full" : $half->contains($i) ? "half" : "";
		            if ($holiday) {
		            	$return .= sprintf("\t%04d-%02d-%02d\t",$year,$month,$day) . "$times\t; ($dow) " . join(", ", @labels) . "\n";
		            }
		        }
		    }
	}
 
	return $return;
}
 
unless (@ARGV == 4)
{
    die "Usage: perl timeperiod_holidays.pl YEAR_START YEAR_END PROFILE TIMES\n";
}
 
my $timeperiod = "define timeperiod{\n\ttimeperiod_name\tholidays\n\talias\tholidays for Date::Calendar-Profile $ARGV[2] from $ARGV[0] to $ARGV[1]\n";
$timeperiod .= print_holidays( @ARGV );
$timeperiod .= "}";
 
print $timeperiod;
 
__END__
