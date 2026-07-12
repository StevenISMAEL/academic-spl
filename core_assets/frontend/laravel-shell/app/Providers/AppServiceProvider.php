<?php

namespace App\Providers;

use Illuminate\Support\ServiceProvider;
use Illuminate\View\ViewFinderInterface;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Register any application services.
     */
    public function register(): void
    {
        $this->app->extend('view.finder', function ($finder, $app) {
            $base = app_path('Modules');
            $mappings = [
                'personas.index' => $base . '/PersonasModule/resources/views/index.blade.php',
                'cursos.index'   => $base . '/CursosModule/resources/views/index.blade.php',
                'periodos.index' => $base . '/PeriodosModule/resources/views/index.blade.php',
                'grading.index'  => $base . '/GradingModule/resources/views/index.blade.php',
                'modules.attendance.index' => $base . '/AttendanceModule/resources/views/index.blade.php',
                'enrollment.index' => $base . '/EnrollmentModule/resources/views/index.blade.php',
                'schedule.index' => $base . '/ScheduleModule/resources/views/index.blade.php',
                'reports.index' => $base . '/ReportsModule/resources/views/index.blade.php',
                'certificates.index' => $base . '/CertificatesModule/resources/views/index.blade.php',
            ];

            return new class($finder, $mappings) implements ViewFinderInterface {
                private ViewFinderInterface $finder;
                private array $mappings;

                public function __construct(ViewFinderInterface $finder, array $mappings)
                {
                    $this->finder = $finder;
                    $this->mappings = $mappings;
                }

                public function find($name)
                {
                    if (isset($this->mappings[$name])) {
                        $path = $this->mappings[$name];
                        if (file_exists($path)) {
                            return $path;
                        }
                    }
                    return $this->finder->find($name);
                }

                public function addLocation($location)
                {
                    $this->finder->addLocation($location);
                }

                public function addNamespace($namespace, $hints)
                {
                    $this->finder->addNamespace($namespace, $hints);
                }

                public function prependNamespace($namespace, $hints)
                {
                    $this->finder->prependNamespace($namespace, $hints);
                }

                public function replaceNamespace($namespace, $hints)
                {
                    $this->finder->replaceNamespace($namespace, $hints);
                }

                public function addExtension($extension)
                {
                    $this->finder->addExtension($extension);
                }

                public function hasHintInformation()
                {
                    return $this->finder->hasHintInformation();
                }

                public function getExtensions()
                {
                    return $this->finder->getExtensions();
                }

                public function flush()
                {
                    $this->finder->flush();
                }
            };
        });
    }

    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        //
    }
}
