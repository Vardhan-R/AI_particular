$sw = [Diagnostics.Stopwatch]::StartNew()

$rating_int = $args[0]

Set-Location ("category_" + $rating_int)

$prev_img_cnt = [int](Get-Content -Path ("category_" + $rating_int + "_image_count.txt"))
$final_img_cnt = $prev_img_cnt + $args[1]

Write-Output ("Final image count: " + $final_img_cnt + ".")

Write-Output $final_img_cnt > ("category_" + $rating_int + "_image_count.txt")

Set-Location ".."

$sw.Stop()
$sw.Elapsed