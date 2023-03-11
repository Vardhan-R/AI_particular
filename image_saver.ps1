$sw = [Diagnostics.Stopwatch]::StartNew()

$rating_int = $args[0]

.\image_link_finder.py $rating_int $args[1]

Set-Location ("category_" + $rating_int)

do {
    $a = Get-Content -Path ("category_" + $rating_int + "_communication.txt")
} while ($a -ne 1)

$prev_img_cnt = [int](Get-Content -Path ("category_" + $rating_int + "_image_count.txt"))
$all_links = Get-Content ("category_" + $rating_int + "_links.txt")
$final_img_cnt = $prev_img_cnt + $all_links.Length

Write-Output ("Final image count: " + $final_img_cnt + ".")

$prev_img_cnt..($final_img_cnt - 1) | ForEach-Object -Parallel {
    # $all_links = $using:all_links
    # $final_img_cnt = $using:final_img_cnt
    # $prev_img_cnt = $using:prev_img_cnt
    Invoke-WebRequest ($using:all_links)[$_ - $using:prev_img_cnt] -OutFile ("category_" + $using:rating_int + "_img_" + $_ + ".jpg")
    Write-Output ("Saved image " + $_ + ".")
} -ThrottleLimit 15

Write-Output $final_img_cnt > ("category_" + $rating_int + "_image_count.txt")

Set-Location ".."

$sw.Stop()
$sw.Elapsed