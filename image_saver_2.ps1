$sw = [Diagnostics.Stopwatch]::StartNew()
.\image_link_finder_2.py $args[0]
do {
    $a = Get-Content -Path ("all_categories_communication.txt")
} while ($a -ne 1)

for ($rating_int = 0; $rating_int -lt 3; $rating_int++) {
    Set-Location ("category_" + $rating_int)

    $prev_img_cnt = [int](Get-Content -Path ("category_" + $rating_int + "_image_count.txt"))
    $all_links = Get-Content ("category_" + $rating_int + "_links.txt")
    $final_img_cnt = $prev_img_cnt + $all_links.Length

    Write-Output ("Final image count of category_" + $rating_int +": " + $final_img_cnt + ".")

    $prev_img_cnt..($final_img_cnt - 1) | ForEach-Object -Parallel {
        $rating_int = $using:rating_int
        Invoke-WebRequest ($using:all_links)[$_ - $using:prev_img_cnt] -OutFile ("category_" + $rating_int + "_img_" + $_ + ".jpg")
        Write-Output ("Saved image " + $_ + " in category_" + $rating_int +".")
    } -ThrottleLimit 15

    Write-Output $final_img_cnt > ("category_" + $rating_int + "_image_count.txt")
    Write-Output ("Final image count of category_" + $rating_int +": " + $final_img_cnt + ".")

    Set-Location ".."
}

$sw.Stop()
$sw.Elapsed